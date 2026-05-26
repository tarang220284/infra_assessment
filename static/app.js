/* WWT Cyber-Recovery Discovery — SPA (auth, RBAC, projects, sessions, audit) */

const API = "/api";
const LS  = window.localStorage;
const state = {
  token:        LS.getItem("ire.token") || null,
  user:         null,
  model:        null,
  projects:     [],
  currentProject: null,
  currentSession: null,
  view: { kind: "overview" },
  saveTimers: {},
};

const $  = (sel) => document.querySelector(sel);
const $$ = (sel) => Array.from(document.querySelectorAll(sel));
const el = (tag, attrs = {}, ...children) => {
  const node = (tag.startsWith("svg:"))
    ? document.createElementNS("http://www.w3.org/2000/svg", tag.slice(4))
    : document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") node.setAttribute("class", v);
    else if (k === "html") node.innerHTML = v;
    else if (k.startsWith("on")) node.addEventListener(k.substring(2).toLowerCase(), v);
    else if (v === false || v == null) {/* skip */}
    else node.setAttribute(k, v);
  }
  for (const c of children) {
    if (c == null) continue;
    node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
  }
  return node;
};

async function api(path, opts = {}, opts2 = {}) {
  const headers = { "Content-Type": "application/json", ...(opts.headers || {}) };
  if (state.token) headers["Authorization"] = "Bearer " + state.token;
  const res = await fetch(API + path, { ...opts, headers });
  if (res.status === 401 && !opts2.allow401) {
    state.token = null; state.user = null;
    LS.removeItem("ire.token");
    showLogin();
    throw new Error("unauthorized");
  }
  if (!res.ok) {
    let msg = `${res.status} ${res.statusText}`;
    try { const body = await res.json(); if (body && body.detail) msg = body.detail; } catch {}
    throw new Error(msg);
  }
  if (res.status === 204) return null;
  const ct = res.headers.get("content-type") || "";
  return ct.includes("json") ? res.json() : res.text();
}

const writeAllowed = () => state.user && (state.user.role === "admin" || state.user.role === "facilitator");
const isAdmin      = () => state.user && state.user.role === "admin";

/* ─────────── boot ─────────── */
(async function init() {
  attachLoginHandlers();
  attachResetHandlers();
  attachHomeHandlers();
  attachWorkspaceHandlers();

  if (state.token) {
    try {
      state.user = await api("/auth/me");
    } catch (e) { state.user = null; }
  }
  if (!state.user) { showLogin(); return; }
  if (state.user.must_reset) { showResetScreen(); return; }
  await afterAuth();
})();

async function afterAuth() {
  // load model + projects
  state.model = await api("/model");
  await loadProjects();
  showHome("projects");
}

/* ─────────── login / reset ─────────── */
function showLogin() {
  $("#login").classList.remove("hidden");
  $("#resetScreen").classList.add("hidden");
  $("#home").classList.add("hidden");
  $("#workspace").classList.add("hidden");
  setTimeout(() => $("#loginUsername").focus(), 50);
}

function attachLoginHandlers() {
  $("#loginForm").addEventListener("submit", async (ev) => {
    ev.preventDefault();
    $("#loginErr").textContent = "";
    const username = $("#loginUsername").value.trim();
    const password = $("#loginPassword").value;
    try {
      const r = await api("/auth/login", { method: "POST", body: JSON.stringify({ username, password }) }, { allow401: true });
      state.token = r.token; state.user = r.user;
      LS.setItem("ire.token", r.token);
      $("#loginPassword").value = "";
      if (state.user.must_reset) { showResetScreen(); }
      else { await afterAuth(); }
    } catch (e) {
      $("#loginErr").textContent = e.message || "Sign-in failed";
    }
  });
}

function showResetScreen() {
  $("#login").classList.add("hidden");
  $("#resetScreen").classList.remove("hidden");
  $("#home").classList.add("hidden");
  $("#workspace").classList.add("hidden");
  $("#resetCurrent").value = ""; $("#resetNew").value = ""; $("#resetConfirm").value = "";
  $("#resetErr").textContent = "Password must be 8+ characters with 1 uppercase, 1 number, and 1 special character.";
  setTimeout(() => $("#resetCurrent").focus(), 50);
}

function attachResetHandlers() {
  $("#resetCancel").addEventListener("click", async () => {
    try { await api("/auth/logout", { method: "POST" }); } catch {}
    state.token = null; state.user = null; LS.removeItem("ire.token");
    showLogin();
  });
  $("#resetForm").addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const cur = $("#resetCurrent").value, nw = $("#resetNew").value, cf = $("#resetConfirm").value;
    if (nw !== cf) { $("#resetErr").textContent = "New password and confirmation do not match."; return; }
    try {
      await api("/auth/reset-password", { method: "POST", body: JSON.stringify({ current_password: cur, new_password: nw }) });
      state.user = await api("/auth/me");
      await afterAuth();
    } catch (e) {
      $("#resetErr").textContent = e.message || "Reset failed";
    }
  });
}

/* ─────────── home screen ─────────── */
function showHome(tab = "projects") {
  $("#login").classList.add("hidden");
  $("#resetScreen").classList.add("hidden");
  $("#home").classList.remove("hidden");
  $("#workspace").classList.add("hidden");
  // user chip
  const chip = $("#userChip");
  chip.textContent = `${state.user.full_name || state.user.username} · ${state.user.role}`;
  chip.classList.toggle("admin", state.user.role === "admin");
  // admin-only tabs
  $$(".admin-only").forEach(n => n.classList.toggle("hidden", !isAdmin()));
  // write-only controls
  $$(".write-only").forEach(n => n.classList.toggle("disabled", !writeAllowed()));
  // tab
  setTab(tab);
}

function setTab(t) {
  $$(".top-tab").forEach(b => b.classList.toggle("active", b.dataset.tab === t));
  $("#tab-projects").classList.toggle("hidden", t !== "projects");
  $("#tab-users").classList.toggle("hidden", t !== "users");
  $("#tab-audit").classList.toggle("hidden", t !== "audit");
  if (t === "projects") renderProjects();
  if (t === "users")    renderUsers();
  if (t === "audit")    renderAudit();
}

function attachHomeHandlers() {
  $$(".top-tab").forEach(b => b.addEventListener("click", () => setTab(b.dataset.tab)));
  $("#logoutBtn").addEventListener("click", async () => {
    try { await api("/auth/logout", { method: "POST" }); } catch {}
    state.token = null; state.user = null; LS.removeItem("ire.token");
    showLogin();
  });
  $("#changePwBtn").addEventListener("click", () => openPasswordChangeModal());
  $("#newProjectBtn").addEventListener("click", () => openProjectModal(null));
  $("#newUserBtn").addEventListener("click", () => openUserModal(null));
  $("#refreshAuditBtn").addEventListener("click", () => renderAudit());
}

/* ─── projects tab ─── */
async function loadProjects() {
  state.projects = await api("/projects");
}

function renderProjects() {
  const grid = $("#projectGrid"); grid.innerHTML = "";
  for (const p of state.projects) {
    const card = el("div", { class: "project-card", onClick: () => openProject(p.id) },
      el("div", { class: "pc-customer" }, p.customer),
      el("div", { class: "pc-name" }, p.name),
      el("div", { class: "pc-desc" }, p.description || "—"),
      el("div", { class: "pc-bar" }),
      el("div", { class: "pc-meta" },
        el("span", {}, `${p.sessions_total} session${p.sessions_total === 1 ? "" : "s"}`),
        el("span", {}, `${p.domains_assessed}/${p.domains_total} domains`),
      ),
    );
    if (writeAllowed()) {
      const actions = el("div", { class: "pc-actions" });
      const editBtn = el("button", { class: "icon-btn edit", title: "Edit",
        onClick: (e) => { e.stopPropagation(); openProjectModal(p); } }, "Edit");
      const delBtn = el("button", { class: "icon-btn", title: "Delete",
        onClick: async (e) => { e.stopPropagation();
          if (!confirm(`Delete project "${p.name}"? All sessions inside will be lost.`)) return;
          await api("/projects/" + p.id, { method: "DELETE" });
          await loadProjects(); renderProjects();
        } }, "Delete");
      actions.appendChild(editBtn); actions.appendChild(delBtn);
      card.appendChild(actions);
    }
    grid.appendChild(card);
  }
  if (writeAllowed()) {
    grid.appendChild(el("div", { class: "project-card new-card", onClick: () => openProjectModal(null) }, "+ New Project"));
  }
  if (state.projects.length === 0 && !writeAllowed()) {
    grid.appendChild(el("div", { class: "empty-state" }, "No projects yet."));
  }
}

/* ─── users tab ─── */
async function renderUsers() {
  if (!isAdmin()) return;
  let users;
  try { users = await api("/admin/users"); }
  catch (e) { $("#userTable").innerHTML = `<div class="empty-state">${e.message}</div>`; return; }
  const t = $("#userTable"); t.innerHTML = "";
  const table = el("table");
  table.appendChild(el("thead", {}, el("tr", {},
    el("th", {}, "Username"), el("th", {}, "Full name"), el("th", {}, "Role"),
    el("th", {}, "Status"), el("th", {}, "Last login"), el("th", {}, ""),
  )));
  const tbody = el("tbody");
  for (const u of users) {
    tbody.appendChild(el("tr", {},
      el("td", {}, u.username),
      el("td", {}, u.full_name || "—"),
      el("td", {}, el("span", { class: "role-pill " + u.role }, u.role)),
      el("td", {}, u.active ? "Active" : el("span", { class: "inactive" }, "Disabled")),
      el("td", {}, u.last_login_at ? u.last_login_at.replace("T", " ").slice(0, 16) : "—"),
      el("td", { class: "actions" },
        el("button", { class: "icon-btn edit", onClick: () => openUserModal(u) }, "Edit"),
        u.id !== state.user.id
          ? el("button", { class: "icon-btn", onClick: async () => {
              if (!confirm(`Delete user "${u.username}"?`)) return;
              await api("/admin/users/" + u.id, { method: "DELETE" });
              renderUsers();
            }}, "Delete")
          : null,
      ),
    ));
  }
  table.appendChild(tbody);
  t.appendChild(table);
}

/* ─── audit tab ─── */
async function renderAudit() {
  if (!isAdmin()) return;
  let data;
  try { data = await api("/admin/audit-logs?limit=200"); }
  catch (e) { $("#auditTable").innerHTML = `<div class="empty-state">${e.message}</div>`; return; }
  const t = $("#auditTable"); t.innerHTML = "";
  const table = el("table");
  table.appendChild(el("thead", {}, el("tr", {},
    el("th", {}, "When"), el("th", {}, "User"), el("th", {}, "Action"),
    el("th", {}, "Target"), el("th", {}, "Detail"),
  )));
  const tbody = el("tbody");
  for (const it of data.items) {
    tbody.appendChild(el("tr", {},
      el("td", {}, (it.created_at || "").replace("T", " ").slice(0, 19)),
      el("td", {}, it.username || "—"),
      el("td", {}, it.action),
      el("td", {}, it.target_type ? `${it.target_type}: ${it.target_id || "—"}` : "—"),
      el("td", { style: "max-width: 480px; word-break: break-word;" }, it.detail || ""),
    ));
  }
  table.appendChild(tbody);
  t.appendChild(table);
}

/* ─────────── modals (project, user, password) ─────────── */
function openModal(title, contentNode) {
  $("#modalTitle").textContent = title;
  const body = $("#modalBody"); body.innerHTML = "";
  body.appendChild(contentNode);
  $("#modal").classList.remove("hidden");
}
function closeModal() { $("#modal").classList.add("hidden"); }

function openProjectModal(existing) {
  if (!writeAllowed()) return;
  const form = el("form");
  const nameIn   = el("input", { required: "", maxlength: "160", value: existing?.name || "" });
  const custIn   = el("input", { required: "", maxlength: "160", value: existing?.customer || "" });
  const descTa   = el("textarea", { placeholder: "Optional one-line description" }, existing?.description || "");
  const errDiv   = el("div", { class: "form-error" });
  form.appendChild(el("label", {}, "Project name", nameIn));
  form.appendChild(el("label", {}, "Customer", custIn));
  form.appendChild(el("label", {}, "Description (optional)", descTa));
  form.appendChild(errDiv);
  form.appendChild(el("div", { class: "row right" },
    el("button", { type: "button", class: "btn", onClick: closeModal }, "Cancel"),
    el("button", { type: "submit", class: "btn btn-primary" }, existing ? "Save" : "Create"),
  ));
  form.onsubmit = async (ev) => {
    ev.preventDefault();
    try {
      const data = { name: nameIn.value.trim(), customer: custIn.value.trim(), description: descTa.value.trim() };
      if (existing) await api("/projects/" + existing.id, { method: "PATCH", body: JSON.stringify(data) });
      else          await api("/projects",                { method: "POST",  body: JSON.stringify(data) });
      closeModal(); await loadProjects(); renderProjects();
    } catch (e) { errDiv.textContent = e.message; }
  };
  openModal(existing ? "Edit project" : "New project", form);
  setTimeout(() => nameIn.focus(), 50);
}

function openUserModal(existing) {
  const form = el("form");
  const usernameIn = el("input", { required: "", maxlength: "120", value: existing?.username || "", disabled: existing ? "" : false });
  const fullnameIn = el("input", { maxlength: "120", value: existing?.full_name || "" });
  const roleSel    = el("select", {},
    el("option", { value: "admin",       selected: existing?.role === "admin"       ? "" : false }, "Admin"),
    el("option", { value: "facilitator", selected: (existing?.role || "facilitator") === "facilitator" ? "" : false }, "Facilitator"),
    el("option", { value: "viewer",      selected: existing?.role === "viewer"      ? "" : false }, "Viewer"),
  );
  const activeChk = el("input", { type: "checkbox" });
  if (!existing || existing.active) activeChk.checked = true;
  const mustResetChk = el("input", { type: "checkbox" });
  if (existing?.must_reset) mustResetChk.checked = true;
  const pwIn  = el("input", { type: "password", placeholder: existing ? "(leave blank to keep)" : "Initial password" });
  const errDiv = el("div", { class: "form-error" });
  form.appendChild(el("label", {}, "Username", usernameIn));
  form.appendChild(el("label", {}, "Full name (optional)", fullnameIn));
  form.appendChild(el("label", {}, "Role", roleSel));
  if (existing) {
    form.appendChild(el("label", { style: "display:flex;align-items:center;gap:6px;font-size:12px;" }, activeChk, "Active"));
    form.appendChild(el("label", { style: "display:flex;align-items:center;gap:6px;font-size:12px;" }, mustResetChk, "Force password reset on next login"));
    form.appendChild(el("label", {}, "Reset password (optional)", pwIn));
  } else {
    form.appendChild(el("label", {}, "Initial password (user will be forced to reset)", pwIn));
  }
  form.appendChild(errDiv);
  form.appendChild(el("div", { class: "row right" },
    el("button", { type: "button", class: "btn", onClick: closeModal }, "Cancel"),
    el("button", { type: "submit", class: "btn btn-primary" }, existing ? "Save" : "Create"),
  ));
  form.onsubmit = async (ev) => {
    ev.preventDefault();
    try {
      if (existing) {
        const patch = {
          full_name:  fullnameIn.value.trim(),
          role:       roleSel.value,
          active:     activeChk.checked,
          must_reset: mustResetChk.checked,
        };
        if (pwIn.value) patch.reset_password = pwIn.value;
        await api("/admin/users/" + existing.id, { method: "PATCH", body: JSON.stringify(patch) });
      } else {
        await api("/admin/users", { method: "POST", body: JSON.stringify({
          username: usernameIn.value.trim(), full_name: fullnameIn.value.trim(),
          role: roleSel.value, initial_password: pwIn.value,
        }) });
      }
      closeModal(); renderUsers();
    } catch (e) { errDiv.textContent = e.message; }
  };
  openModal(existing ? "Edit user" : "New user", form);
  setTimeout(() => (existing ? fullnameIn : usernameIn).focus(), 50);
}

function openPasswordChangeModal() {
  const form = el("form");
  const cur = el("input", { type: "password", required: "" });
  const nw  = el("input", { type: "password", required: "" });
  const cf  = el("input", { type: "password", required: "" });
  const err = el("div", { class: "form-error" }, "8+ chars · 1 uppercase · 1 number · 1 special character");
  form.appendChild(el("label", {}, "Current password", cur));
  form.appendChild(el("label", {}, "New password", nw));
  form.appendChild(el("label", {}, "Confirm new password", cf));
  form.appendChild(err);
  form.appendChild(el("div", { class: "row right" },
    el("button", { type: "button", class: "btn", onClick: closeModal }, "Cancel"),
    el("button", { type: "submit", class: "btn btn-primary" }, "Update"),
  ));
  form.onsubmit = async (ev) => {
    ev.preventDefault();
    if (nw.value !== cf.value) { err.textContent = "New password and confirmation do not match."; return; }
    try {
      await api("/auth/reset-password", { method: "POST", body: JSON.stringify({ current_password: cur.value, new_password: nw.value }) });
      closeModal();
    } catch (e) { err.textContent = e.message; }
  };
  openModal("Change password", form);
  setTimeout(() => cur.focus(), 50);
}

/* ─────────── workspace (open project) ─────────── */
async function openProject(pid) {
  state.currentProject = await api("/projects/" + pid);
  state.currentSession = state.currentProject.sessions[0] ? await api("/sessions/" + state.currentProject.sessions[0].id) : null;
  state.view = state.currentSession ? { kind: "dashboard" } : { kind: "overview" };

  $("#login").classList.add("hidden");
  $("#home").classList.add("hidden");
  $("#workspace").classList.remove("hidden");

  $("#brandProject").textContent  = state.currentProject.name;
  $("#brandCustomer").textContent = state.currentProject.customer;

  // disable write controls if not allowed
  $$(".write-only").forEach(n => n.classList.toggle("disabled", !writeAllowed()));

  renderSessionSelect();
  renderDomainBadge();
  renderSidebarNav();
  renderProgressFooter();
  renderView();
}

function attachWorkspaceHandlers() {
  $("#backToHome").addEventListener("click", async () => {
    state.currentProject = null; state.currentSession = null;
    await loadProjects();
    showHome("projects");
  });
  $("#sessionSelect").addEventListener("change", async (e) => {
    if (!e.target.value) return;
    state.currentSession = await api("/sessions/" + e.target.value);
    state.view = { kind: "dashboard" };
    renderDomainBadge(); renderSidebarNav(); renderProgressFooter(); renderView();
  });
  $$("[data-view='dashboard']").forEach(b => b.addEventListener("click", () => {
    if (!state.currentSession) return;
    state.view = { kind: "dashboard" }; renderView(); renderSidebarNav();
  }));
  $$("[data-view='overview']").forEach(b => b.addEventListener("click", () => {
    state.view = { kind: "overview" }; renderView(); renderSidebarNav();
  }));
  $$("[data-export]").forEach(b => b.addEventListener("click", () => {
    if (!state.currentSession) return;
    downloadExport(state.currentSession.id, b.getAttribute("data-export"));
  }));
  $("#searchBox").addEventListener("input", e => {
    const q = e.target.value.trim().toLowerCase();
    const results = $("#searchResults"); results.innerHTML = "";
    if (!q || !state.currentSession) return;
    const d = currentDomain();
    for (const layer of d.layers) for (const question of layer.questions) {
      const hay = (question.primary + " " + question.sub_questions.join(" ")).toLowerCase();
      if (hay.includes(q)) {
        results.appendChild(el("div", {
          class: "search-result",
          onClick: () => {
            state.view = { kind: "question", qid: question.id };
            renderView(); renderSidebarNav();
            results.innerHTML = ""; e.target.value = "";
          },
        }, el("span", { class: "sr-q" }, `Q${question.id}`), question.primary));
      }
    }
  });
}

async function downloadExport(sid, fmt) {
  // Fetch with auth header → blob → save
  const res = await fetch(`${API}/sessions/${sid}/export/${fmt}`, { headers: { "Authorization": "Bearer " + state.token } });
  if (!res.ok) { alert("Export failed: " + res.status); return; }
  const blob = await res.blob();
  const filename = (res.headers.get("Content-Disposition") || "").match(/filename="([^"]+)"/)?.[1] || `export.${fmt}`;
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a"); a.href = url; a.download = filename;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function openNewSessionModal() {
  if (!writeAllowed()) return;
  // collect domains already used in this project
  const usedDomains = new Set(state.currentProject.sessions.map(s => s.domain));
  const form = el("form");
  const sel = el("select", { required: "" });
  for (const key of state.model.domain_order) {
    const d = state.model.domains[key];
    const tag = usedDomains.has(key) ? "  (already exists)" : "";
    sel.appendChild(el("option", { value: key }, `${d.label}${tag}`));
  }
  const errDiv = el("div", { class: "form-error" }, "Session will be auto-named after the domain. Customer is inherited from the project.");
  form.appendChild(el("label", {}, "Domain", sel));
  form.appendChild(errDiv);
  form.appendChild(el("div", { class: "row right" },
    el("button", { type: "button", class: "btn", onClick: closeModal }, "Cancel"),
    el("button", { type: "submit", class: "btn btn-primary" }, "Create"),
  ));
  form.onsubmit = async (ev) => {
    ev.preventDefault();
    try {
      const s = await api("/sessions", { method: "POST", body: JSON.stringify({ project_id: state.currentProject.id, domain: sel.value }) });
      closeModal();
      state.currentProject = await api("/projects/" + state.currentProject.id);
      state.currentSession = await api("/sessions/" + s.id);
      state.view = { kind: "dashboard" };
      renderSessionSelect(); renderDomainBadge(); renderSidebarNav(); renderProgressFooter(); renderView();
    } catch (e) { errDiv.textContent = e.message; }
  };
  openModal("New session", form);
}

function currentDomain() {
  return state.currentSession ? state.model.domains[state.currentSession.domain] : null;
}

function renderSessionSelect() {
  const sel = $("#sessionSelect"); sel.innerHTML = "";
  if (!state.currentProject) return;
  // refresh latest sessions in project
  const sessions = state.currentProject.sessions || [];
  for (const dkey of state.model.domain_order) {
    const inDomain = sessions.filter(s => s.domain === dkey);
    if (!inDomain.length) continue;
    const og = el("optgroup", { label: state.model.domains[dkey].label });
    for (const s of inDomain) {
      const o = el("option", { value: s.id }, s.name);
      if (state.currentSession && state.currentSession.id === s.id) o.selected = true;
      og.appendChild(o);
    }
    sel.appendChild(og);
  }
  if (!sessions.length) sel.appendChild(el("option", {}, "(no sessions yet)"));
}

function renderDomainBadge() {
  const badge = $("#domainBadge"); badge.innerHTML = "";
  if (!state.currentSession) return;
  const d = currentDomain();
  badge.appendChild(el("span", { class: "domain-pill domain-" + state.currentSession.domain }, d.label));
}

function renderSidebarNav() {
  const nav = $("#layerNav"); nav.innerHTML = "";
  if (!state.currentSession) return;
  const d = currentDomain();
  const prog = state.currentSession.progress.by_layer;
  for (const layer of d.layers) {
    const lp = prog[layer.id] || { total: 0, complete: 0 };
    const group = el("div", { class: "layer-group" });
    const head = el("button", {
      class: "nav-link" + (state.view.kind === "layer" && state.view.layerId === layer.id ? " active" : ""),
      onClick: () => { state.view = { kind: "layer", layerId: layer.id }; renderView(); renderSidebarNav(); },
    });
    head.appendChild(el("div", { class: "layer-head" },
      el("span", {}, `L${layer.id} · ${layer.title}`),
      el("span", { class: "pct" }, `${lp.complete}/${lp.total}`),
    ));
    group.appendChild(head);
    for (const q of layer.questions) {
      const sub = el("button", {
        class: "nav-sub" + (state.view.kind === "question" && state.view.qid === q.id ? " active" : ""),
        onClick: () => { state.view = { kind: "question", qid: q.id }; renderView(); renderSidebarNav(); },
      }, `Q${q.id}. ${q.primary.slice(0, 70)}${q.primary.length > 70 ? "…" : ""}`);
      group.appendChild(sub);
    }
    nav.appendChild(group);
  }
  $$("[data-view='dashboard']").forEach(b => b.classList.toggle("active", state.view.kind === "dashboard"));
  $$("[data-view='overview']").forEach(b => b.classList.toggle("active", state.view.kind === "overview"));
}

function renderProgressFooter() {
  const foot = $("#progressOverall"); foot.innerHTML = "";
  if (!state.currentSession) { foot.appendChild(el("div", {}, "No session selected.")); return; }
  const p = state.currentSession.progress;
  foot.appendChild(el("div", {}, `${p.answers_complete}/${p.answers_total} complete (${p.overall_pct}%)`));
  const bar = el("div", { class: "progress-bar" }, el("div", { style: `width:${p.overall_pct}%` }));
  foot.appendChild(bar);
  foot.appendChild(el("div", {}, `Open follow-ups: ${p.open_follow_ups}${p.answers_na ? ` · N/A: ${p.answers_na}` : ""}`));
}

/* ─────────── views ─────────── */
function renderView() {
  const view = $("#view"); view.innerHTML = "";
  if (state.view.kind === "overview")  return renderProjectOverview(view);
  if (!state.currentSession) { view.appendChild(el("div", { class: "empty-state" }, "No session yet. Click + New on the sidebar.")); return; }
  if (state.view.kind === "dashboard") return renderDashboard(view);
  if (state.view.kind === "layer")     return renderLayer(view, state.view.layerId);
  if (state.view.kind === "question")  return renderQuestion(view, state.view.qid);
}

async function renderProjectOverview(view) {
  const p = state.currentProject;
  view.appendChild(el("div", { class: "view-header" },
    el("h1", {}, `Project Overview — ${p.name}`),
    el("div", { class: "sub" }, `${p.customer}${p.description ? " · " + p.description : ""}`),
  ));
  const summary = await api("/projects/" + p.id + "/summary");

  const stats = el("div", { class: "dash-summary" });
  stats.appendChild(stat("Customer", p.customer, ""));
  stats.appendChild(stat("Infrastructure maturity", summary.infra_avg ?? "—", "of 5"));
  stats.appendChild(stat("Domains assessed", `${summary.domains_assessed}/${summary.domains_total}`, ""));
  const followUps = summary.per_domain.reduce((n, d) => n + (d.progress?.open_follow_ups || 0), 0);
  stats.appendChild(stat("Open follow-ups", followUps, "across all domains"));
  view.appendChild(stats);

  view.appendChild(el("h2", { style: "font-size:14px;margin:18px 0 6px;color:var(--text-dim)" }, "Overall Infrastructure Level — radar across domains"));
  const radarCard = el("div", { class: "radar-card radar" });
  radarCard.appendChild(buildRadar(
    state.model.domain_order.map(k => {
      const e = summary.per_domain.find(x => x.domain === k);
      return { label: state.model.domains[k].label, value: e ? e.overall_avg : null };
    }),
    { fillClass: "dark" }
  ));
  view.appendChild(radarCard);

  view.appendChild(el("h2", { style: "font-size:14px;margin:18px 0 6px;color:var(--text-dim)" }, "Per-domain status"));
  const og = el("div", { class: "overview-grid" });
  for (const dkey of state.model.domain_order) {
    const d = state.model.domains[dkey];
    const entry = summary.per_domain.find(x => x.domain === dkey);
    const missing = !entry;
    og.appendChild(el("div", {
      class: "overview-card" + (missing ? " missing" : ""),
      onClick: async () => {
        if (entry) {
          state.currentSession = await api("/sessions/" + entry.session_id);
          state.view = { kind: "dashboard" };
          renderSessionSelect(); renderDomainBadge(); renderSidebarNav(); renderProgressFooter(); renderView();
        } else if (writeAllowed()) {
          openNewSessionModalFor(dkey);
        }
      },
    },
      el("div", { class: "ov-label" }, d.label),
      el("div", { class: "ov-value" }, missing ? "—" : `${entry.overall_avg ?? "—"}/5`),
      el("div", { class: "ov-sub" }, missing
        ? (writeAllowed() ? "no session — click to create" : "no session")
        : `${entry.progress.answers_complete}/${entry.progress.answers_total} complete · ${entry.progress.open_follow_ups} follow-ups`),
    ));
  }
  view.appendChild(og);
}

function openNewSessionModalFor(domainKey) {
  if (!writeAllowed()) return;
  api("/sessions", { method: "POST", body: JSON.stringify({ project_id: state.currentProject.id, domain: domainKey }) })
    .then(async (s) => {
      state.currentProject = await api("/projects/" + state.currentProject.id);
      state.currentSession = await api("/sessions/" + s.id);
      state.view = { kind: "dashboard" };
      renderSessionSelect(); renderDomainBadge(); renderSidebarNav(); renderProgressFooter(); renderView();
    })
    .catch(e => alert("Create failed: " + e.message));
}

async function renderDashboard(view) {
  const d = currentDomain();
  view.appendChild(el("div", { class: "view-header" },
    el("h1", {}, `${d.title} — Dashboard`),
    el("div", { class: "sub" }, `${state.currentSession.name} · ${state.currentProject.customer} · ${d.label}`),
  ));
  const summary = await api("/sessions/" + state.currentSession.id + "/summary");

  const stats = el("div", { class: "dash-summary" });
  stats.appendChild(stat("Overall maturity", summary.overall_avg ?? "—", "of 5"));
  stats.appendChild(stat("Complete", `${summary.progress.answers_complete}/${summary.progress.answers_total}`, `${summary.progress.overall_pct}%`));
  stats.appendChild(stat("Open follow-ups", summary.progress.open_follow_ups, ""));
  stats.appendChild(stat("Not applicable", summary.progress.answers_na || 0, "excluded from scoring"));
  view.appendChild(stats);

  // radars side-by-side
  const wrap = el("div", { class: "radar-wrap" });
  const r1 = el("div", { class: "radar-card radar" },
    el("h3", {}, "Maturity by layer"),
    el("div", { class: "radar-sub" }, "5-axis radar — one axis per facilitator layer"),
  );
  r1.appendChild(buildRadar(summary.by_layer.map(b => ({ label: `L${b.layer_id} ${short(b.title)}`, value: b.avg_score }))));
  wrap.appendChild(r1);

  let proj;
  try { proj = await api("/projects/" + state.currentProject.id + "/summary"); }
  catch { proj = { per_domain: [] }; }
  const r2 = el("div", { class: "radar-card radar" },
    el("h3", {}, "Overall Infrastructure Level"),
    el("div", { class: "radar-sub" }, `Maturity across this project's assessed domains`),
  );
  r2.appendChild(buildRadar(
    state.model.domain_order.map(k => {
      const e = proj.per_domain.find(x => x.domain === k);
      return { label: state.model.domains[k].label, value: e ? e.overall_avg : null };
    }),
    { fillClass: "dark" }
  ));
  wrap.appendChild(r2);
  view.appendChild(wrap);

  view.appendChild(el("h2", { style: "font-size:14px;margin:18px 0 6px;color:var(--text-dim)" }, "Layer averages"));
  const bars = el("div", { class: "layer-bars" });
  for (const row of summary.by_layer) {
    const pct = row.avg_score ? (row.avg_score / 5) * 100 : 0;
    bars.appendChild(el("div", { class: "layer-bar" },
      el("div", {}, `L${row.layer_id}`),
      el("div", {}, row.title),
      el("div", { class: "bar-track" }, el("div", { class: "bar-fill", style: `width:${pct}%` })),
      el("div", { style: "text-align:right" }, row.avg_score == null ? "—" : `${row.avg_score}/5`),
    ));
  }
  view.appendChild(bars);

  view.appendChild(el("h2", { style: "font-size:14px;margin:24px 0 6px;color:var(--text-dim)" }, `Maturity heatmap — all ${summary.heatmap.length} questions`));
  const grid = el("div", { class: "dash-grid" });
  for (const row of summary.heatmap) {
    let cellClass = "dash-cell ";
    if (row.not_applicable) cellClass += "na";
    else if (row.score) cellClass += "m" + row.score;
    else cellClass += "unanswered";
    grid.appendChild(el("div", {
      class: cellClass,
      onClick: () => { state.view = { kind: "question", qid: row.question_id }; renderView(); renderSidebarNav(); },
      title: row.primary,
    },
      el("div", { class: "qid" }, `Q${row.question_id} · L${row.layer_id}`),
      el("div", { class: "qtext" }, row.primary.slice(0, 90) + (row.primary.length > 90 ? "…" : "")),
      el("div", { class: "qmaturity" },
        row.maturity_label || "—",
        row.follow_up === "open" && !row.not_applicable ? el("span", { class: "followup", style: "margin-left:6px" }, "● follow-up") : null,
      ),
    ));
  }
  view.appendChild(grid);
}

function short(t) { return t.length > 24 ? t.slice(0, 24) + "…" : t; }
function stat(label, value, sub) {
  return el("div", { class: "dash-stat" },
    el("div", { class: "label" }, label),
    el("div", { class: "value" }, String(value)),
    el("div", { class: "sub" }, sub || ""),
  );
}

/* radar (SVG) */
function buildRadar(points, opts = {}) {
  const N = points.length, MAX = 5;
  const W = 480, H = 380, cx = W / 2, cy = H / 2 + 8, R = Math.min(W, H * 0.85) * 0.36;
  const svg = el("svg:svg", { viewBox: `0 0 ${W} ${H}`, xmlns: "http://www.w3.org/2000/svg" });
  for (let r = 1; r <= MAX; r++) {
    svg.appendChild(el("svg:polygon", { points: polyFromValues(Array(N).fill(r), cx, cy, R, MAX), class: r === MAX ? "ring ring-hot" : "ring" }));
  }
  for (let i = 0; i < N; i++) {
    const a = angleAt(i, N);
    const x2 = cx + Math.cos(a) * R, y2 = cy + Math.sin(a) * R;
    svg.appendChild(el("svg:line", { x1: cx, y1: cy, x2, y2, class: "axis" }));
    const lx = cx + Math.cos(a) * (R + 22), ly = cy + Math.sin(a) * (R + 22);
    const parts = splitLabel(points[i].label);
    const t = el("svg:text", { x: lx, y: ly, class: "label", "dominant-baseline": "middle" });
    t.appendChild(el("svg:tspan", { x: lx, dy: parts.length === 1 ? "0" : "-0.5em" }, parts[0]));
    if (parts[1]) t.appendChild(el("svg:tspan", { x: lx, dy: "1.05em", class: "lbl-line2" }, parts[1]));
    svg.appendChild(t);
  }
  for (let r = 1; r <= MAX; r++) {
    svg.appendChild(el("svg:text", { x: cx + 3, y: cy - (r / MAX) * R + 3, class: "scale-label" }, String(r)));
  }
  const values = points.map(p => p.value);
  const filled = values.map(v => v == null ? 0 : v);
  svg.appendChild(el("svg:polygon", { points: polyFromValues(filled, cx, cy, R, MAX), class: `score-fill ${opts.fillClass || ""}` }));
  for (let i = 0; i < N; i++) {
    if (values[i] == null) continue;
    const a = angleAt(i, N), rad = (values[i] / MAX) * R;
    svg.appendChild(el("svg:circle", { cx: cx + Math.cos(a) * rad, cy: cy + Math.sin(a) * rad, r: 3, class: "score-pt" }));
  }
  return svg;
}
function angleAt(i, N) { return -Math.PI / 2 + (i / N) * Math.PI * 2; }
function polyFromValues(vals, cx, cy, R, MAX) {
  return vals.map((v, i) => {
    const a = angleAt(i, vals.length); const rad = (v / MAX) * R;
    return (cx + Math.cos(a) * rad).toFixed(1) + "," + (cy + Math.sin(a) * rad).toFixed(1);
  }).join(" ");
}
function splitLabel(s) {
  if (s.length <= 18) return [s];
  const mid = Math.floor(s.length / 2);
  let cut = s.lastIndexOf(" ", mid + 4);
  if (cut < 6) cut = s.indexOf(" ", mid);
  if (cut < 0) return [s];
  return [s.slice(0, cut), s.slice(cut + 1)];
}

/* layer / question */
function renderLayer(view, layerId) {
  const d = currentDomain();
  const layer = d.layers.find(l => l.id === layerId);
  view.appendChild(el("div", { class: "view-header" },
    el("h1", {}, `Layer ${layer.id}: ${layer.title}`),
    el("div", { class: "sub" }, `${d.label} · Questions ${layer.questions[0].id}–${layer.questions[layer.questions.length-1].id}`),
  ));
  view.appendChild(el("div", { class: "layer-intent" }, layer.intent));
  for (const q of layer.questions) view.appendChild(buildQuestionCard(q, layer));
}

function renderQuestion(view, qid) {
  const d = currentDomain();
  const layer = d.layers.find(l => l.questions.some(q => q.id === qid));
  const q = layer.questions.find(q => q.id === qid);
  view.appendChild(el("div", { class: "view-header" },
    el("h1", {}, `Q${q.id}`),
    el("div", { class: "sub" }, `${d.label} · Layer ${layer.id}: ${layer.title}`),
  ));
  view.appendChild(buildQuestionCard(q, layer, { expandSubs: true }));
}

function buildQuestionCard(q, layer, { expandSubs = false } = {}) {
  const d = currentDomain();
  const a = state.currentSession.answers.find(x => x.question_id === q.id) || {};
  const isNA = !!a.not_applicable;
  const readOnly = !writeAllowed();
  const card = el("section", { class: "q-card scroll-target" + (isNA ? " na" : ""), id: `q-${q.id}` });

  card.appendChild(el("div", { class: "q-head" },
    el("div", {},
      el("div", { class: "q-layer-tag" }, `${d.label} · Layer ${layer.id} · Q${q.id}`),
      el("h3", { class: "q-primary" }, q.primary),
    ),
    el("div", {},
      el("span", { class: `status-pill ${isNA ? "status-na" : "status-" + (a.status || "unanswered")}` },
        isNA ? "N/A" : (a.status || "unanswered").replace("_", " ")),
    ),
  ));

  if (q.id === 1 && layer.id === 1) {
    card.appendChild(el("div", { class: "facilitator-callout" }, d.facilitator_intro));
  }

  const naToggle = el("label", { class: "na-toggle" + (isNA ? " active" : "") });
  const naCheckbox = el("input", { type: "checkbox", disabled: readOnly ? "" : false });
  naCheckbox.checked = isNA;
  naCheckbox.addEventListener("change", () => scheduleSave(q.id, "not_applicable", naCheckbox.checked, saveHint, true));
  naToggle.appendChild(naCheckbox);
  naToggle.appendChild(document.createTextNode("Not applicable (excluded from rating)"));
  card.appendChild(naToggle);

  const subBox = el("div", { class: "subq-list" });
  const subUl = el("ul");
  for (const sq of q.sub_questions) subUl.appendChild(el("li", {}, sq));
  subBox.appendChild(subUl);
  if (!expandSubs) subBox.style.display = "none";
  const toggle = el("button", { class: "subq-toggle",
    onClick: () => {
      const show = subBox.style.display === "none";
      subBox.style.display = show ? "block" : "none";
      toggle.textContent = show ? "Hide probing sub-questions" : `Show probing sub-questions (${q.sub_questions.length})`;
    },
  }, expandSubs ? "Hide probing sub-questions" : `Show probing sub-questions (${q.sub_questions.length})`);
  card.appendChild(el("div", { style: "margin-top:8px" }, toggle));
  card.appendChild(subBox);

  const responseTa   = el("textarea", { placeholder: "Capture the client's response…", disabled: readOnly ? "" : false }, a.response || "");
  const evidenceTa   = el("textarea", { placeholder: "Evidence pointers, doc references, quotes…", style: "min-height:60px", disabled: readOnly ? "" : false }, a.evidence || "");
  const followNoteTa = el("textarea", { placeholder: "Why does this need follow-up? With whom? By when?", style: "min-height:60px", disabled: readOnly ? "" : false }, a.follow_up_note || "");

  const maturitySel = el("select", { disabled: (isNA || readOnly) ? "" : false },
    el("option", { value: "" }, "— maturity rating —"),
    ...state.model.maturity_scale.map(m =>
      el("option", { value: m.value, selected: a.maturity === m.value ? "" : false, title: m.definition },
        `${m.score}. ${m.label} — ${m.definition}`)
    ),
  );
  const statusSel = el("select", { disabled: readOnly ? "" : false },
    ...state.model.answer_states.map(s =>
      el("option", { value: s, selected: (a.status || "unanswered") === s ? "" : false }, s.replace("_", " "))),
  );
  const followSel = el("select", { disabled: (isNA || readOnly) ? "" : false },
    ...state.model.follow_up_states.map(s =>
      el("option", { value: s, selected: (a.follow_up || "none") === s ? "" : false }, s)),
  );
  const ownerIn = el("input", { type: "text", value: a.owner || "", placeholder: "Owner (e.g. infra lead)", disabled: readOnly ? "" : false });

  const saveHint = el("div", { class: "save-hint" }, "");

  const bindAutoSave = (input, field) => {
    if (readOnly) return;
    const ev = input.tagName === "SELECT" ? "change" : "input";
    input.addEventListener(ev, () => scheduleSave(q.id, field, input.value, saveHint));
  };
  bindAutoSave(responseTa,   "response");
  bindAutoSave(evidenceTa,   "evidence");
  bindAutoSave(followNoteTa, "follow_up_note");
  bindAutoSave(maturitySel,  "maturity");
  bindAutoSave(statusSel,    "status");
  bindAutoSave(followSel,    "follow_up");
  bindAutoSave(ownerIn,      "owner");

  card.appendChild(el("div", { class: "fields" },
    el("div", { class: "field-block" }, el("label", {}, "Response"), responseTa),
    el("div", { class: "field-block" },
      el("div", { class: "field-row" },
        el("div", { class: "field-block" }, el("label", {}, "Maturity"),  maturitySel),
        el("div", { class: "field-block" }, el("label", {}, "Status"),    statusSel),
      ),
      el("div", { class: "field-row" },
        el("div", { class: "field-block" }, el("label", {}, "Owner"),     ownerIn),
        el("div", { class: "field-block" }, el("label", {}, "Follow-up"), followSel),
      ),
      el("div", { class: "field-block" }, el("label", {}, "Evidence / notes"), evidenceTa),
      el("div", { class: "field-block" }, el("label", {}, "Follow-up note"), followNoteTa),
    ),
  ));
  card.appendChild(saveHint);
  return card;
}

function scheduleSave(qid, field, value, hintEl, reloadCard = false) {
  const key = `${qid}:${field}`;
  if (state.saveTimers[key]) clearTimeout(state.saveTimers[key]);
  hintEl.textContent = "saving…"; hintEl.classList.remove("saved");
  state.saveTimers[key] = setTimeout(async () => {
    try {
      const body = (field === "not_applicable") ? { not_applicable: !!value } : { [field]: value };
      const updated = await api(`/sessions/${state.currentSession.id}/answers/${qid}`, { method: "PATCH", body: JSON.stringify(body) });
      const i = state.currentSession.answers.findIndex(a => a.question_id === qid);
      state.currentSession.answers[i] = updated;
      const s = await api(`/sessions/${state.currentSession.id}`);
      state.currentSession.progress = s.progress;
      renderProgressFooter();
      renderSidebarNav();
      hintEl.textContent = "saved"; hintEl.classList.add("saved");
      setTimeout(() => { hintEl.textContent = ""; hintEl.classList.remove("saved"); }, 1200);
      if (reloadCard) renderView();
    } catch (e) {
      hintEl.textContent = "save failed: " + e.message;
    }
  }, 350);
}
