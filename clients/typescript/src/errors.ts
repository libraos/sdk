/**
 * Typed errors mirroring `components.schemas.Error` in the partner OpenAPI spec.
 * The spec's Error.type enum is the canonical machine-readable kind; HTTP status
 * is carried alongside for callers that branch on the wire status.
 */

/** Discriminator values for the partner `Error.type` field. */
export type LibraOSErrorType =
  | "invalid_request_error"
  | "authentication_error"
  | "permission_error"
  | "not_found_error"
  | "rate_limit_error"
  | "billing_error"
  | "upstream_error"
  | "vertex_schema_error"
  | "validation_error"
  | "internal_error";

/** The JSON body LibraOS returns on an error response. */
export interface LibraOSErrorBody {
  type: LibraOSErrorType | string;
  message: string;
  param?: string;
  /** Machine-readable subcode (e.g. "credits_exhausted"). */
  code?: string;
  /** Seconds — present on rate_limit_error. */
  retry_after?: number;
  /** Present on vertex_schema_error — the offending tool. */
  tool_name?: string;
  /** Present on vertex_schema_error — JSON path to the offending parameter. */
  parameter_path?: string;
  /** Human-readable hint for actionable errors. */
  fix_hint?: string;
}

/** Error thrown by the typed client for any non-2xx REST response. */
export class LibraOSApiError extends Error {
  readonly status: number;
  readonly type: LibraOSErrorType | string;
  readonly code?: string;
  readonly retryAfter?: number;
  readonly body?: LibraOSErrorBody;

  constructor(status: number, body?: LibraOSErrorBody, fallbackMessage?: string) {
    super(body?.message ?? fallbackMessage ?? `LibraOS request failed (HTTP ${status})`);
    this.name = "LibraOSApiError";
    this.status = status;
    this.type = body?.type ?? "internal_error";
    this.code = body?.code;
    this.retryAfter = body?.retry_after;
    this.body = body;
  }

  /** True when the failure is an auth/token problem (401, authentication_error). */
  get isAuth(): boolean {
    return this.status === 401 || this.type === "authentication_error";
  }
}

/** Coerce an unknown openapi-fetch error payload into a {@link LibraOSErrorBody}. */
export function asLibraOSErrorBody(raw: unknown): LibraOSErrorBody | undefined {
  if (raw && typeof raw === "object" && "message" in raw) {
    return raw as LibraOSErrorBody;
  }
  return undefined;
}
