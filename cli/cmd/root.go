// Package cmd holds the cobra command tree for libraos-cli.
package cmd

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

// Shared global flags resolved by every subcommand via globalConfig().
var (
	flagProfile string
	flagURL     string
	flagAPIKey  string
	flagJSON    bool
)

// rootCmd is the entry point for `libraos-cli ...`.
var rootCmd = &cobra.Command{
	Use:          "libraos-cli",
	Short:        "LibraOS partner CLI — sync agents/employees, validate, test webhook callbacks",
	SilenceUsage: true, // failed runs don't dump full --help spam
}

// Execute runs the root command. Called from main.go.
func Execute() {
	if err := rootCmd.Execute(); err != nil {
		os.Exit(1)
	}
}

func init() {
	rootCmd.PersistentFlags().StringVar(&flagProfile, "profile", "", "Profile in ~/.libraos/config.yaml (overrides LIBRAOS_PROFILE)")
	rootCmd.PersistentFlags().StringVar(&flagURL, "url", "", "LibraOS server URL (overrides profile + LIBRAOS_BASE_URL)")
	rootCmd.PersistentFlags().StringVar(&flagAPIKey, "api-key", "", "Bearer token (overrides profile + LIBRAOS_API_KEY)")
	rootCmd.PersistentFlags().BoolVar(&flagJSON, "json", false, "Emit one JSON object per record on stdout (default: human table)")
}

// globalConfig resolves --url + --api-key in this priority order:
// explicit flag -> env -> profile -> discovery hint.
func globalConfig() (url string, apiKey string, err error) {
	url = flagURL
	if url == "" {
		url = os.Getenv("LIBRAOS_BASE_URL")
	}
	apiKey = flagAPIKey
	if apiKey == "" {
		apiKey = os.Getenv("LIBRAOS_API_KEY")
	}

	if url == "" || apiKey == "" {
		profileName := flagProfile
		if profileName == "" {
			profileName = os.Getenv("LIBRAOS_PROFILE")
		}
		if profile, ok := loadProfile(profileName); ok {
			if url == "" {
				url = profile.URL
			}
			if apiKey == "" && profile.APIKeyEnv != "" {
				apiKey = os.Getenv(profile.APIKeyEnv)
			}
		}
	}

	if url == "" {
		return "", "", fmt.Errorf("server URL not set (use --url, LIBRAOS_BASE_URL, or a profile in ~/.libraos/config.yaml)")
	}
	if apiKey == "" {
		return "", "", fmt.Errorf("api-key not set (use --api-key, LIBRAOS_API_KEY, or a profile pointing at an env var)")
	}
	return url, apiKey, nil
}

// Profile mirrors one entry under profiles: in ~/.libraos/config.yaml.
type Profile struct {
	URL         string `yaml:"url"          mapstructure:"url"`
	APIKeyEnv   string `yaml:"api_key_env"  mapstructure:"api_key_env"`
	CallbackURL string `yaml:"callback_url" mapstructure:"callback_url"`
}

// loadProfile reads ~/.libraos/config.yaml. If profileName is empty, uses
// the file's `default:` field. Returns ok=false silently if file missing
// or profile not found.
func loadProfile(profileName string) (Profile, bool) {
	home, err := os.UserHomeDir()
	if err != nil {
		return Profile{}, false
	}
	cfgPath := filepath.Join(home, ".libraos", "config.yaml")
	if _, err := os.Stat(cfgPath); err != nil {
		return Profile{}, false
	}

	v := viper.New()
	v.SetConfigFile(cfgPath)
	v.SetConfigType("yaml")
	if err := v.ReadInConfig(); err != nil {
		return Profile{}, false
	}

	if profileName == "" {
		profileName = v.GetString("default")
	}
	if profileName == "" {
		return Profile{}, false
	}

	prefix := "profiles." + profileName
	if !v.IsSet(prefix) {
		return Profile{}, false
	}
	return Profile{
		URL:         v.GetString(prefix + ".url"),
		APIKeyEnv:   strings.TrimSpace(v.GetString(prefix + ".api_key_env")),
		CallbackURL: v.GetString(prefix + ".callback_url"),
	}, true
}
