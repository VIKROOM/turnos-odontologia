import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { APP_NAME } from "./lib/constants";

const rootElement = document.getElementById("root");
if (rootElement === null) {
  throw new Error("No se encontró #root");
}

createRoot(rootElement).render(
  <StrictMode>
    <main>
      <h1>{APP_NAME}</h1>
    </main>
  </StrictMode>,
);
