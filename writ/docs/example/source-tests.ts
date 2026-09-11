import { describe, it, expect } from "vitest";
import { borrow, returnCopy, shelfState } from "./lending";

// The identifier in the test name is the whole mechanism. The ledger reads these names out of
// the suite; nothing else marks a requirement as proven, and no work order can talk it into it.

describe("lending", () => {
  it("[FR-LEND-01] lends a copy that is on the shelf to the person who asked", () => {
    const loan = borrow({ copy: "c1", person: "ana" });
    expect(loan.person).toBe("ana");
    expect(shelfState("c1")).toBe("out");
  });

  it("[INV-001] refuses a second borrow of a copy already out, naming the holder", () => {
    borrow({ copy: "c1", person: "ana" });
    expect(() => borrow({ copy: "c1", person: "ben" })).toThrow(/held by ana/);
  });
});
