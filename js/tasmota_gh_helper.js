import { Octokit, App } from "https://esm.sh/octokit";

window.octokit = new Octokit();

const r = await window.octokit.request("GET /repos/{owner}/{repo}/releases", {
    owner: "tasmota",
    repo: "install",
    per_page: 999
  });

window.rel = r.data

console.log("Releases:", r.data);

// export octokit as octo;
