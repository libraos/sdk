// Package sign produces Stripe-style HMAC-SHA256 signatures for
// outgoing test-callback webhooks. The signing scheme matches the
// receiver-side verification in libraos.callbacks.WebhookRouter
// (Python SDK):
//
//	signed input = "<unix_ts>.<tool_use_id>.<body>"
//	header value = "t=<unix_ts>,v1=<hex(hmac_sha256(secret, signed_input))>"
//
// Binding tool_use_id into the HMAC defeats idempotency-key tampering
// (a malicious party can't reuse a valid signature with a different key).
package sign

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"net/http"
	"strconv"
	"time"
)

// Header names. The server sends both the LibraOS names and the older
// X-Nova-* ones during the rename, so test callbacks do the same: a
// receiver written against either name verifies them.
const (
	SignatureHeader         = "X-LibraOS-Signature"
	IdempotencyKeyHeader    = "X-LibraOS-Idempotency-Key"
	LegacySignatureHeader   = "X-Nova-Signature"
	LegacyIdempotencyHeader = "X-Nova-Idempotency-Key"
)

// SetHeaders sets the signature and idempotency-key headers under both
// the new and the legacy names.
func SetHeaders(h http.Header, signature, toolUseID string) {
	h.Set(SignatureHeader, signature)
	h.Set(IdempotencyKeyHeader, toolUseID)
	h.Set(LegacySignatureHeader, signature)
	h.Set(LegacyIdempotencyHeader, toolUseID)
}

// Sign returns the signature header value (`t=<unix>,v1=<hex>`).
func Sign(secret, toolUseID string, body []byte, now time.Time) string {
	ts := strconv.FormatInt(now.Unix(), 10)
	mac := hmac.New(sha256.New, []byte(secret))
	mac.Write([]byte(ts))
	mac.Write([]byte("."))
	mac.Write([]byte(toolUseID))
	mac.Write([]byte("."))
	mac.Write(body)
	return fmt.Sprintf("t=%s,v1=%s", ts, hex.EncodeToString(mac.Sum(nil)))
}
