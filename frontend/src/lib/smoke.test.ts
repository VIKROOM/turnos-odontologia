import { describe, expect, it } from "vitest";
import { APP_NAME } from "./constants";

describe("smoke", () => {
  it("expone el nombre de la aplicación", () => {
    expect(APP_NAME).toBe("turnos-odontologia");
  });

  it("el nombre es un identificador slug usable en URLs", () => {
    expect(APP_NAME).toMatch(/^[a-z0-9-]+$/);
  });
});
