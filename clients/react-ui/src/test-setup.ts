import { afterEach } from "vitest";
import { cleanup } from "@testing-library/react";

// @testing-library/react's automatic afterEach(cleanup) only registers when
// it finds a global `afterEach` (e.g. Jest, or Vitest with `test.globals:
// true`). This project imports test functions explicitly instead of using
// globals, so cleanup is wired up here to keep each test's DOM isolated.
afterEach(cleanup);
