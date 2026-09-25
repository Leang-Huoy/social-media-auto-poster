let currentUser = null;
let allAccounts = [];
let attachedPhotoPath = '';
let attachedPhotoUrl = '';
let attachedVideoPath = '';
let attachedVideoUrl = '';

document.addEventListener('DOMContentLoaded', () => {
  checkAuth();
  initLoginHandlers();
  initTabs();
  initEditor();
  initMediaUploads();
  initAccountModal();
  initUserModal();
  initMobileModal();
});

// Toast Helper
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  const icon = type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️';
  toast.innerHTML = `<span>${icon}</span> <span style="white-space: pre-wrap;">${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 4500);
}

// =========================================================================
// AUTH & LOGIN / LOGOUT
// =========================================================================
async function checkAuth() {
  try {
    const res = await fetch('/api/me');
    const data = await res.json();
    if (data.logged_in && data.user) {
      currentUser = data.user;
      showApp();
    } else {
      showLogin();
    }
  } catch (err) {
    showLogin();
  }
}

function showLogin() {
  currentUser = null;
  document.getElementById('loginScreen').style.display = 'flex';
  document.getElementById('mainAppContent').style.display = 'none';

  // Clear inputs on login screen
  clearAuthFields();

  // Reset to login form view
  document.getElementById('loginForm').style.display = 'flex';
  document.getElementById('registerForm').style.display = 'none';
  document.getElementById('authCardTitle').textContent = 'ចូលប្រើប្រាស់ប្រព័ន្ធ';
  document.getElementById('authCardSub').textContent = 'Social Poster Pro Management';
}

function clearAuthFields() {
  const loginUser = document.getElementById('loginUsername');
  const loginPass = document.getElementById('loginPassword');
  const chkLogin = document.getElementById('chkShowLoginPassword');
  if (loginUser) loginUser.value = '';
  if (loginPass) {
    loginPass.value = '';
    loginPass.type = 'password';
  }
  if (chkLogin) chkLogin.checked = false;

  const regUser = document.getElementById('regUsername');
  const regName = document.getElementById('regFullName');
  const regPass = document.getElementById('regPassword');
  const chkReg = document.getElementById('chkShowRegPassword');
  if (regUser) regUser.value = '';
  if (regName) regName.value = '';
  if (regPass) {
    regPass.value = '';
    regPass.type = 'password';
  }
  if (chkReg) chkReg.checked = false;
}

function showApp() {
  document.getElementById('loginScreen').style.display = 'none';
  document.getElementById('mainAppContent').style.display = 'flex';

  // Update User Header Info
  const roleBadge = document.getElementById('userRoleBadge');
  const nameDisplay = document.getElementById('userNameDisplay');
  nameDisplay.textContent = currentUser.name || currentUser.username;

  if (currentUser.role === 'admin') {
    roleBadge.className = 'role-pill admin';
    roleBadge.innerHTML = '👑 Admin';
    document.querySelectorAll('.admin-only-feature').forEach(el => el.style.display = 'inline-flex');
    document.getElementById('tabNavUsers').style.display = 'inline-flex';
    document.getElementById('accountPermissionNotice').textContent = 
      '🔑 លោកអ្នកមានសិទ្ធិពេញលេញជា Admin ក្នុងការបន្ថែម កែសម្រួល និងតេស្តគណនីបណ្ដាញសង្គម។';
  } else {
    roleBadge.className = 'role-pill user';
    roleBadge.innerHTML = '👤 User (បុគ្គលិក)';
    document.querySelectorAll('.admin-only-feature').forEach(el => el.style.display = 'none');
    document.getElementById('tabNavUsers').style.display = 'none';
    document.getElementById('accountPermissionNotice').textContent = 
      '🔒 លោកអ្នកជា User (សិទ្ធិប្រើប្រាស់) អាចមើល និង Post តាមបណ្ដាញសង្គមដែល Admin បានកំណត់ជូន។';
  }

  loadAccounts();
  loadQueue();
  loadLogs();
}

function initLoginHandlers() {
  // Show / Hide Password Checkbox for Login
  document.getElementById('chkShowLoginPassword')?.addEventListener('change', (e) => {
    const passInput = document.getElementById('loginPassword');
    if (passInput) passInput.type = e.target.checked ? 'text' : 'password';
  });

  // Show / Hide Password Checkbox for Register
  document.getElementById('chkShowRegPassword')?.addEventListener('change', (e) => {
    const passInput = document.getElementById('regPassword');
    if (passInput) passInput.type = e.target.checked ? 'text' : 'password';
  });

  // Switch between Login and Register views
  document.getElementById('btnSwitchToRegister')?.addEventListener('click', () => {
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('registerForm').style.display = 'flex';
    document.getElementById('authCardTitle').textContent = 'បង្កើតគណនីថ្មី';
    document.getElementById('authCardSub').textContent = 'ចុះឈ្មោះគណនីបុគ្គលិក (Staff)';
    clearAuthFields();
  });

  document.getElementById('btnSwitchToLogin')?.addEventListener('click', () => {
    document.getElementById('registerForm').style.display = 'none';
    document.getElementById('loginForm').style.display = 'flex';
    document.getElementById('authCardTitle').textContent = 'ចូលប្រើប្រាស់ប្រព័ន្ធ';
    document.getElementById('authCardSub').textContent = 'Social Poster Pro Management';
    clearAuthFields();
  });

  // Login Form Submit
  document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const u = document.getElementById('loginUsername').value.trim();
    const p = document.getElementById('loginPassword').value.trim();

    const btn = document.getElementById('btnLoginSubmit');
    btn.disabled = true;
    btn.innerHTML = `<span class="spinner"></span> កំពុងផ្ទៀងផ្ទាត់...`;

    try {
      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: u, password: p })
      });
      const data = await res.json();
      if (data.success && data.user) {
        currentUser = data.user;
        showToast(`🎉 ស្វាគមន៍ការចូលប្រើប្រាស់, ${data.user.name}!`, 'success');
        showApp();
      } else {
        showToast(data.error || 'ការ Login បរាជ័យ!', 'error');
      }
    } catch (err) {
      showToast('Error: ' + err.message, 'error');
    } finally {
      btn.disabled = false;
      btn.innerHTML = `<span>🔐</span> ចូលប្រើប្រាស់ (Login)`;
    }
  });

  // Register Form Submit
  document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const u = document.getElementById('regUsername').value.trim();
    const name = document.getElementById('regFullName').value.trim();
    const p = document.getElementById('regPassword').value.trim();

    const btn = document.getElementById('btnRegisterSubmit');
    btn.disabled = true;
    btn.innerHTML = `<span class="spinner"></span> កំពុងបង្កើតគណនី...`;

    try {
      const res = await fetch('/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: u, password: p, name: name })
      });
      const data = await res.json();
      if (data.success && data.user) {
        currentUser = data.user;
        showToast(`🎉 បង្កើតគណនីជោគជ័យ! ស្វាគមន៍ ${data.user.name}!`, 'success');
        showApp();
      } else {
        showToast(data.error || 'ការចុះឈ្មោះបរាជ័យ!', 'error');
      }
    } catch (err) {
      showToast('Error: ' + err.message, 'error');
    } finally {
      btn.disabled = false;
      btn.innerHTML = `<span>✨</span> បង្កើតគណនី (Create Account)`;
    }
  });

  // Logout Button (Clears credentials)
  document.getElementById('btnLogout')?.addEventListener('click', async () => {
    try {
      await fetch('/api/logout', { method: 'POST' });
    } catch (e) {}
    showToast('បានចាកចេញពីគណនីរួចរាល់', 'info');
    showLogin();
  });
}

// =========================================================================
// TABS
// =========================================================================
function initTabs() {
  const navTabs = document.querySelectorAll('.nav-tab');
  navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.dataset.tab;
      document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
      tab.classList.add('active');
      const pane = document.getElementById(target);
      if (pane) pane.classList.add('active');

      if (target === 'queueTab') loadQueue();
      if (target === 'logsTab') loadLogs();
      if (target === 'accountsTab') renderAccountsCards();
      if (target === 'userManagementTab' && currentUser?.role === 'admin') loadUsersList();
    });
  });
}

// =========================================================================
// ACCOUNTS MANAGEMENT & SELECTION
// =========================================================================
async function loadAccounts() {
  try {
    const res = await fetch('/api/accounts');
    if (res.status === 401) {
      showLogin();
      return;
    }
    allAccounts = await res.json();

    const activeCount = allAccounts.filter(a => a.enabled !== false).length;
    document.getElementById('activeAccountsCount').textContent = `${activeCount} គណនីសកម្ម / សរុប ${allAccounts.length}`;
    document.getElementById('tabAccCount').textContent = allAccounts.length;

    renderAccountsSelection();
    renderAccountsCards();
  } catch (err) {
    console.error('Failed to load accounts:', err);
  }
}

function getPlatformIcon(platform) {
  switch (platform.toLowerCase()) {
    case 'telegram': return '✈️';
    case 'facebook': return '🌐';
    case 'youtube': return '▶️';
    case 'tiktok': return '🎵';
    default: return '📢';
  }
}

function renderAccountsSelection() {
  const container = document.getElementById('accountsCheckboxList');
  if (!allAccounts.length) {
    container.innerHTML = `<p style="color: var(--text-dim); font-size: 0.85rem;">មិនទាន់មានគណនីនៅឡើយទេ។</p>`;
    return;
  }

  container.innerHTML = allAccounts.map(acc => `
    <label class="account-checkbox-chip ${acc.enabled !== false ? 'active' : ''}" for="acc_chk_${acc.id}">
      <input type="checkbox" id="acc_chk_${acc.id}" value="${acc.id}" ${acc.enabled !== false ? 'checked' : ''}>
      <span class="acc-icon">${getPlatformIcon(acc.platform)}</span>
      <div class="acc-text">
        <span class="acc-name">${acc.name}</span>
        <span class="acc-platform-tag">${acc.platform.toUpperCase()} ${acc.type ? '(' + acc.type + ')' : ''}</span>
      </div>
    </label>
  `).join('');

  container.querySelectorAll('input[type="checkbox"]').forEach(chk => {
    chk.addEventListener('change', () => {
      chk.closest('.account-checkbox-chip').classList.toggle('active', chk.checked);
      updateMockupChannel();
    });
  });

  updateMockupChannel();
}

function updateMockupChannel() {
  const checked = document.querySelectorAll('#accountsCheckboxList input[type="checkbox"]:checked');
  const mockupName = document.getElementById('mockupChannelName');
  if (checked.length === 0) {
    mockupName.textContent = 'គ្មានគណនីត្រូវបានជ្រើសរើស';
  } else if (checked.length === 1) {
    const acc = allAccounts.find(a => a.id === checked[0].value);
    mockupName.textContent = acc ? acc.name : 'Social Media Broadcast';
  } else {
    mockupName.textContent = `បានជ្រើសរើស ${checked.length} គណនី`;
  }
}

function renderAccountsCards() {
  const container = document.getElementById('accountsCardsGrid');
  if (!container) return;

  if (!allAccounts.length) {
    container.innerHTML = `<p style="color: var(--text-dim); grid-column: 1/-1; text-align: center; padding: 2rem;">មិនទាន់មានគណនីនៅឡើយទេ។</p>`;
    return;
  }

  const isAdmin = currentUser?.role === 'admin';

  container.innerHTML = allAccounts.map(acc => {
    const p = acc.platform.toLowerCase();
    const details = isAdmin ? (
      p === 'telegram' ? `Chat ID: ${acc.chat_id || 'N/A'}` :
      p === 'facebook' ? `Page ID: ${acc.page_id || 'N/A'}` :
      p === 'youtube' ? `Client ID: ${acc.client_id ? '✓ កំណត់រួច' : 'N/A'}` :
      `Token: ${acc.tiktok_access_token ? '✓ កំណត់រួច' : 'N/A'}`
    ) : 'កំណត់ដោយ Admin';

    // Actions only shown for Admin
    const actionsHtml = isAdmin ? `
      <div class="account-card-actions">
        <button class="btn-sm" onclick="testAccount('${acc.id}')" title="តេស្តការតភ្ជាប់">🔍 តេស្ត</button>
        <button class="btn-sm" onclick="toggleAccount('${acc.id}')">${acc.enabled ? 'បិទ' : 'បើក'}</button>
        <button class="btn-sm" style="color: var(--danger-color);" onclick="deleteAccount('${acc.id}')" title="លុបគណនី">🗑️ លុប</button>
      </div>
    ` : `
      <div style="font-size: 0.75rem; color: var(--text-dim); margin-top: auto;">
        ✓ អាចប្រើសម្រាប់ Publish បាន
      </div>
    `;

    return `
      <div class="glass-panel account-card">
        <div class="account-card-header">
          <span class="account-platform-badge ${p}">
            ${getPlatformIcon(p)} ${acc.platform.toUpperCase()}
          </span>
          <span style="font-size: 0.75rem; color: ${acc.enabled !== false ? 'var(--success-color)' : 'var(--text-dim)'}; font-weight: 600;">
            ${acc.enabled !== false ? '🟢 សកម្ម' : '⚪ អសកម្ម'}
          </span>
        </div>

        <div>
          <h4 style="font-size: 1rem; font-weight: 700; color: #fff;">${acc.name}</h4>
          <p style="font-size: 0.78rem; color: var(--text-dim); margin-top: 4px;">${details}</p>
        </div>

        ${actionsHtml}
      </div>
    `;
  }).join('');
}

window.testAccount = async function(id) {
  if (currentUser?.role !== 'admin') return;
  showToast('កំពុងតេស្តការតភ្ជាប់...', 'info');
  try {
    const res = await fetch(`/api/accounts/${id}/test`, { method: 'POST' });
    const data = await res.json();
    if (data.connected) {
      showToast(`✅ ភ្ជាប់ជោគជ័យ! (${data.name || 'OK'})`, 'success');
    } else {
      showToast(`❌ បរាជ័យ: ${data.error || 'Connection Failed'}`, 'error');
    }
  } catch (err) {
    showToast('Error: ' + err.message, 'error');
  }
};

window.toggleAccount = async function(id) {
  if (currentUser?.role !== 'admin') return;
  const acc = allAccounts.find(a => a.id === id);
  if (!acc) return;
  acc.enabled = !acc.enabled;
  try {
    await fetch(`/api/accounts/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ enabled: acc.enabled })
    });
    loadAccounts();
  } catch (err) {
    showToast('បរាជ័យក្នុងការកែប្រែ', 'error');
  }
};

window.deleteAccount = async function(id) {
  if (currentUser?.role !== 'admin') return;
  if (!confirm('តើអ្នកប្រាកដជាចង់លុបគណនីនេះ?')) return;
  try {
    const res = await fetch(`/api/accounts/${id}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
      showToast('បានលុបគណនីរួចរាល់', 'success');
      loadAccounts();
    }
  } catch (err) {
    showToast('បរាជ័យក្នុងការលុប', 'error');
  }
};

// =========================================================================
// USER MANAGEMENT (ADMIN ONLY)
// =========================================================================
async function loadUsersList() {
  const tbody = document.getElementById('usersTableBody');
  if (!tbody || currentUser?.role !== 'admin') return;

  tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-dim);">កំពុងទាញយកបញ្ជី User...</td></tr>`;
  try {
    const res = await fetch('/api/users');
    const users = await res.json();
    if (!users.length) {
      tbody.innerHTML = `<tr><td colspan="5" style="text-align: center;">មិនមានទិន្នន័យ</td></tr>`;
      return;
    }

    tbody.innerHTML = users.map(u => `
      <tr>
        <td style="font-weight: 700;">${u.username}</td>
        <td>${u.name}</td>
        <td>
          <span class="role-pill ${u.role}">${u.role === 'admin' ? '👑 Admin' : '👤 User (Staff)'}</span>
        </td>
        <td style="font-size: 0.8rem; color: var(--text-dim);">${u.created_at || 'N/A'}</td>
        <td>
          ${u.username === 'admin' ? '<span style="color: var(--text-dim); font-size: 0.75rem;">(Admin ចម្បង)</span>' : `
            <button class="btn-danger-sm" onclick="deleteUserAccount('${u.id}')">លុប</button>
          `}
        </td>
      </tr>
    `).join('');
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="5" style="color: var(--danger-color);">Error Loading Users</td></tr>`;
  }
}

window.deleteUserAccount = async function(id) {
  if (!confirm('តើអ្នកពិតជាចង់លុបគណនីអ្នកប្រើប្រាស់នេះមែនទេ?')) return;
  try {
    const res = await fetch(`/api/users/${id}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
      showToast('បានលុប User ជោគជ័យ!', 'success');
      loadUsersList();
    } else {
      showToast(data.error || 'បរាជ័យក្នុងការលុប!', 'error');
    }
  } catch (err) {
    showToast('Error: ' + err.message, 'error');
  }
};

function initUserModal() {
  const modal = document.getElementById('userModal');
  const btnOpen = document.getElementById('btnOpenAddUserModal');
  const btnClose = document.getElementById('btnCloseUserModal');
  const btnCancel = document.getElementById('btnCancelUserModal');
  const form = document.getElementById('userForm');

  btnOpen?.addEventListener('click', () => {
    form.reset();
    modal.style.display = 'flex';
  });

  const closeModal = () => modal.style.display = 'none';
  btnClose?.addEventListener('click', closeModal);
  btnCancel?.addEventListener('click', closeModal);

  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      username: document.getElementById('newUserUsername').value.trim(),
      password: document.getElementById('newUserPassword').value.trim(),
      name: document.getElementById('newUserName').value.trim(),
      role: document.getElementById('newUserRole').value
    };

    try {
      const res = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (data.success) {
        showToast('បានបង្កើតគណនីអ្នកប្រើប្រាស់ថ្មីជោគជ័យ!', 'success');
        closeModal();
        loadUsersList();
      } else {
        showToast(data.error || 'បរាជ័យក្នុងការបង្កើត!', 'error');
      }
    } catch (err) {
      showToast('Error: ' + err.message, 'error');
    }
  });
}

// =========================================================================
// EDITOR, MEDIA, PUBLISH
// =========================================================================
function initEditor() {
  const textarea = document.getElementById('postMessage');
  const previewText = document.getElementById('previewText');
  const charCounter = document.getElementById('charCount');

  textarea?.addEventListener('input', () => {
    const val = textarea.value;
    previewText.textContent = val || 'សាររបស់អ្នកនឹងបង្ហាញនៅទីនេះពេលអ្នកវាយបញ្ចូល...';
    charCounter.textContent = `${val.length} តួអក្សរ`;
  });

  document.querySelectorAll('.btn-emoji').forEach(b => {
    b.addEventListener('click', () => {
      const emoji = b.textContent;
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const text = textarea.value;
      textarea.value = text.substring(0, start) + emoji + text.substring(end);
      textarea.focus();
      textarea.selectionStart = textarea.selectionEnd = start + emoji.length;
      textarea.dispatchEvent(new Event('input'));
    });
  });

  document.getElementById('btnSelectAll')?.addEventListener('click', () => {
    document.querySelectorAll('#accountsCheckboxList input[type="checkbox"]').forEach(chk => {
      chk.checked = true;
      chk.closest('.account-checkbox-chip').classList.add('active');
    });
    updateMockupChannel();
  });

  document.getElementById('btnDeselectAll')?.addEventListener('click', () => {
    document.querySelectorAll('#accountsCheckboxList input[type="checkbox"]').forEach(chk => {
      chk.checked = false;
      chk.closest('.account-checkbox-chip').classList.remove('active');
    });
    updateMockupChannel();
  });

  document.getElementById('btnPublishNow')?.addEventListener('click', publishNow);
  document.getElementById('btnAddToQueue')?.addEventListener('click', addToQueue);
}

function initMediaUploads() {
  const photoDrop = document.getElementById('photoDropzone');
  const photoInput = document.getElementById('photoFileInput');
  photoDrop?.addEventListener('click', () => photoInput.click());
  photoInput?.addEventListener('change', () => {
    if (photoInput.files.length) uploadMediaFile(photoInput.files[0], 'photo');
  });

  const videoDrop = document.getElementById('videoDropzone');
  const videoInput = document.getElementById('videoFileInput');
  videoDrop?.addEventListener('click', () => videoInput.click());
  videoInput?.addEventListener('change', () => {
    if (videoInput.files.length) uploadMediaFile(videoInput.files[0], 'video');
  });

  document.getElementById('btnRemovePhoto')?.addEventListener('click', () => {
    attachedPhotoPath = '';
    attachedPhotoUrl = '';
    document.getElementById('photoPreviewContainer').style.display = 'none';
    document.getElementById('photoDropzone').style.display = 'block';
    document.getElementById('photoFileInput').value = '';
    document.getElementById('mockupPhoto').style.display = 'none';
  });

  document.getElementById('btnRemoveVideo')?.addEventListener('click', () => {
    attachedVideoPath = '';
    attachedVideoUrl = '';
    document.getElementById('videoPreviewContainer').style.display = 'none';
    document.getElementById('videoDropzone').style.display = 'block';
    document.getElementById('videoFileInput').value = '';
    document.getElementById('mockupVideo').style.display = 'none';
  });
}

async function uploadMediaFile(file, type) {
  const formData = new FormData();
  formData.append('file', file);
  showToast(`កំពុង Upload ${type === 'photo' ? 'រូបភាព' : 'វីដេអូ'}...`, 'info');

  try {
    const res = await fetch('/api/upload', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    if (data.success) {
      if (type === 'photo') {
        attachedPhotoPath = data.file_path;
        attachedPhotoUrl = data.url;
        document.getElementById('photoPreviewImg').src = data.url;
        document.getElementById('photoPreviewContainer').style.display = 'block';
        document.getElementById('photoDropzone').style.display = 'none';
        document.getElementById('mockupPhotoImg').src = data.url;
        document.getElementById('mockupPhoto').style.display = 'block';
      } else {
        attachedVideoPath = data.file_path;
        attachedVideoUrl = data.url;
        document.getElementById('videoPreviewVid').src = data.url;
        document.getElementById('videoPreviewContainer').style.display = 'block';
        document.getElementById('videoDropzone').style.display = 'none';
        document.getElementById('mockupVideoVid').src = data.url;
        document.getElementById('mockupVideo').style.display = 'block';
      }
      showToast(`Upload ${type} ជោគជ័យ!`, 'success');
    } else {
      showToast(data.error || 'Upload បរាជ័យ!', 'error');
    }
  } catch (err) {
    showToast('Upload Error: ' + err.message, 'error');
  }
}

async function publishNow() {
  const message = document.getElementById('postMessage').value.trim();
  const tiktokUrl = document.getElementById('tiktokPublicUrl').value.trim();

  const checkedBoxes = document.querySelectorAll('#accountsCheckboxList input[type="checkbox"]:checked');
  const accountIds = Array.from(checkedBoxes).map(cb => cb.value);

  if (!accountIds.length) {
    showToast('សូមជ្រើសរើសគណនីបណ្ដាញសង្គមយ៉ាងហោចមួយ!', 'error');
    return;
  }

  if (!message && !attachedPhotoPath && !attachedVideoPath) {
    showToast('សូមបញ្ចូលសារ អត្ថបទ រូបភាព ឬ វីដេអូ!', 'error');
    return;
  }

  const btn = document.getElementById('btnPublishNow');
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span> កំពុង Publish...`;

  try {
    const res = await fetch('/api/post', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        photo_path: attachedPhotoPath,
        video_path: attachedVideoPath,
        tiktok_url: tiktokUrl,
        account_ids: accountIds
      })
    });

    const data = await res.json();
    if (data.success) {
      showToast('🎉 បាន Post ទៅកាន់គណនីជោគជ័យ!', 'success');
      if (data.results) {
        const details = Object.values(data.results)
          .map(r => `${r.account_name} (${r.platform}): ${r.success ? '✅ ' + (r.posted_items || []).join('+') : '❌ ' + (r.error || '')}`)
          .join('\n');
        showToast(details, 'info');
      }
      document.getElementById('postMessage').value = '';
      document.getElementById('previewText').textContent = 'សាររបស់អ្នកនឹងបង្ហាញនៅទីនេះពេលអ្នកវាយបញ្ចូល...';
    } else {
      showToast(data.error || 'Post បរាជ័យ!', 'error');
    }
  } catch (err) {
    showToast('Error: ' + err.message, 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = `🚀 Publish ទៅគ្រប់គណនីដែលបានជ្រើសរើស`;
    loadLogs();
  }
}

async function addToQueue() {
  const message = document.getElementById('postMessage').value.trim();
  const tiktokUrl = document.getElementById('tiktokPublicUrl').value.trim();

  const checkedBoxes = document.querySelectorAll('#accountsCheckboxList input[type="checkbox"]:checked');
  const accountIds = Array.from(checkedBoxes).map(cb => cb.value);

  if (!accountIds.length) {
    showToast('សូមជ្រើសរើសគណនី!', 'error');
    return;
  }

  try {
    const res = await fetch('/api/queue', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        photo_path: attachedPhotoPath,
        video_path: attachedVideoPath,
        tiktok_url: tiktokUrl,
        account_ids: accountIds
      })
    });
    const data = await res.json();
    if (data.success) {
      showToast('បានដាក់ចូលក្នុងតារាងរង់ចាំ (Queue) រួចរាល់!', 'success');
    }
  } catch (err) {
    showToast('បរាជ័យក្នុងការដាក់ចូល Queue', 'error');
  }
}

// =========================================================================
// QUEUE & LOGS
// =========================================================================
async function loadQueue() {
  const tbody = document.getElementById('queueTableBody');
  if (!tbody) return;
  tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-dim);">កំពុងទាញយក...</td></tr>`;

  try {
    const res = await fetch('/api/queue');
    const queue = await res.json();
    if (!queue.length) {
      tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-dim);">មិនទាន់មាន Post ក្នុង Queue នៅឡើយទេ</td></tr>`;
      return;
    }

    tbody.innerHTML = queue.map(item => `
      <tr>
        <td>#${item.id}</td>
        <td style="max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${item.content || '(Media Post)'}</td>
        <td>${item.photo_path ? '🖼️ Photo ' : ''}${item.video_path ? '🎬 Video' : ''}</td>
        <td><span class="status-tag ${item.status}">${item.status === 'published' ? '✅ Published' : '⏳ Pending'}</span></td>
        <td>
          <button class="btn-danger-sm" onclick="deleteQueueItem(${item.id})">លុប</button>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="5" style="color: var(--danger-color);">Error Loading Queue</td></tr>`;
  }
}

window.deleteQueueItem = async function(id) {
  if (!confirm('តើអ្នកប្រាកដជាចង់លុប Post នេះចេញពី Queue?')) return;
  try {
    const res = await fetch(`/api/queue/${id}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
      showToast('បានលុបជោគជ័យ!', 'success');
      loadQueue();
    }
  } catch (err) {
    showToast('បរាជ័យក្នុងការលុប!', 'error');
  }
};

async function loadLogs() {
  const container = document.getElementById('logsContainer');
  if (!container) return;

  try {
    const res = await fetch('/api/logs');
    const logs = await res.json();
    if (!logs.length) {
      container.innerHTML = `<p style="color: var(--text-dim); text-align: center; padding: 2rem;">មិនទាន់មានប្រវត្តិ Post នៅឡើយទេ</p>`;
      return;
    }

    container.innerHTML = logs.map(l => `
      <div style="display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; border-bottom: 1px solid var(--border-color);">
        <div style="display: flex; align-items: center; gap: 12px;">
          <span style="font-size: 1.1rem;">${l.status === 'success' ? '✅' : '❌'}</span>
          <div>
            <div style="font-weight: 600; font-size: 0.9rem;">
              ${l.platform} 
              <span style="font-size: 0.72rem; color: var(--accent-cyan); margin-left: 6px;">[ដោយ: ${l.user || 'User'}]</span>
              - <span style="font-weight: 400; color: var(--text-muted);">${l.message}</span>
            </div>
            <div style="font-size: 0.75rem; color: var(--text-dim);">${l.details || ''}</div>
          </div>
        </div>
        <div style="font-size: 0.78rem; color: var(--text-dim);">${l.timestamp}</div>
      </div>
    `).join('');
  } catch (err) {
    container.innerHTML = `<p style="color: var(--danger-color);">Error Loading Logs</p>`;
  }
}

// =========================================================================
// ACCOUNT MODAL (ADMIN ONLY)
// =========================================================================
function initAccountModal() {
  const modal = document.getElementById('accountModal');
  const btnOpen = document.getElementById('btnOpenAddAccountModal');
  const btnClose = document.getElementById('btnCloseModal');
  const btnCancel = document.getElementById('btnCancelModal');
  const platformSelect = document.getElementById('acc_platform');
  const form = document.getElementById('accountForm');

  btnOpen?.addEventListener('click', () => {
    form.reset();
    document.getElementById('acc_id').value = '';
    updateModalPlatformFields();
    modal.style.display = 'flex';
  });

  const closeModal = () => modal.style.display = 'none';
  btnClose?.addEventListener('click', closeModal);
  btnCancel?.addEventListener('click', closeModal);

  platformSelect?.addEventListener('change', updateModalPlatformFields);

  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (currentUser?.role !== 'admin') {
      showToast('មានតែ Admin ទេដែលអាចបន្ថែមគណនីបាន!', 'error');
      return;
    }

    const platform = platformSelect.value;
    const name = document.getElementById('acc_name').value.trim();

    const payload = {
      platform,
      name,
      chat_id: document.getElementById('acc_tg_chat_id').value.trim(),
      bot_token: document.getElementById('acc_tg_token').value.trim(),
      page_id: document.getElementById('acc_fb_page_id').value.trim(),
      access_token: document.getElementById('acc_fb_token').value.trim(),
      client_id: document.getElementById('acc_yt_client_id').value.trim(),
      client_secret: document.getElementById('acc_yt_client_secret').value.trim(),
      refresh_token: document.getElementById('acc_yt_refresh_token').value.trim(),
      tiktok_access_token: document.getElementById('acc_tt_token').value.trim()
    };

    try {
      const res = await fetch('/api/accounts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (data.success) {
        showToast('បានបន្ថែមគណនីថ្មីដោយជោគជ័យ!', 'success');
        closeModal();
        loadAccounts();
      } else {
        showToast(data.error || 'បរាជ័យ!', 'error');
      }
    } catch (err) {
      showToast('Error: ' + err.message, 'error');
    }
  });
}

function updateModalPlatformFields() {
  const platform = document.getElementById('acc_platform').value;
  document.getElementById('fields_telegram').style.display = platform === 'telegram' ? 'block' : 'none';
  document.getElementById('fields_facebook').style.display = platform === 'facebook' ? 'block' : 'none';
  document.getElementById('fields_youtube').style.display = platform === 'youtube' ? 'block' : 'none';
  document.getElementById('fields_tiktok').style.display = platform === 'tiktok' ? 'block' : 'none';
}

// =========================================================================
// PWA INSTALLATION (SERVICE WORKER & BEFOREINSTALLPROMPT)
// =========================================================================
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').then((reg) => {
      console.log('PWA ServiceWorker registered with scope:', reg.scope);
    }).catch((err) => {
      console.log('PWA ServiceWorker registration failed:', err);
    });
  });
}

let deferredInstallPrompt = null;
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredInstallPrompt = e;
  const btnInstall = document.getElementById('btnInstallPwa');
  if (btnInstall) btnInstall.style.display = 'inline-flex';
});

document.getElementById('btnInstallPwa')?.addEventListener('click', async () => {
  if (deferredInstallPrompt) {
    deferredInstallPrompt.prompt();
    const { outcome } = await deferredInstallPrompt.userChoice;
    if (outcome === 'accepted') {
      showToast('🎉 អបអរសាទរ! App ត្រូវបានដំឡើងជោគជ័យលើទូរស័ព្ទ!', 'success');
    }
    deferredInstallPrompt = null;
    const btn = document.getElementById('btnInstallPwa');
    if (btn) btn.style.display = 'none';
  } else {
    showToast('💡 សម្រាប់ iPhone សូមចុច Share ➡️ Add to Home Screen', 'info');
  }
});

// =========================================================================
// MOBILE PHONE ACCESS MODAL (QR CODE, LOCAL WI-FI & ONLINE TUNNEL)
// =========================================================================
function initMobileModal() {
  const modal = document.getElementById('mobileAccessModal');
  const btnOpen = document.getElementById('btnOpenMobileModal');
  const btnClose = document.getElementById('btnCloseMobileModal');
  const btnCopy = document.getElementById('btnCopyMobileUrl');
  const urlInput = document.getElementById('mobileUrlInput');
  const qrImg = document.getElementById('mobileQrCodeImg');
  const tabPublic = document.getElementById('tabModePublic');
  const tabLocal = document.getElementById('tabModeLocal');
  const notice = document.getElementById('mobileModalNotice');
  const btnTunnel = document.getElementById('btnLaunchPublicTunnel');

  let currentMode = 'public';
  let networkData = null;

  async function refreshNetworkInfo() {
    try {
      const res = await fetch('/api/network-info');
      networkData = await res.json();
      updateModalDisplay();
    } catch (e) {
      if (urlInput) urlInput.value = `http://${window.location.hostname}:5000`;
    }
  }

  function updateModalDisplay() {
    if (!networkData) return;
    if (currentMode === 'public') {
      if (networkData.public_url) {
        urlInput.value = networkData.public_url;
        qrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=${networkData.public_url}`;
        notice.textContent = '🌐 ដំណើរការអនឡាញ: ប្រើបានពីគ្រប់ទីកន្លែងលើពិភពលោកតាម 4G/5G';
        btnTunnel.style.display = 'none';
      } else {
        urlInput.value = 'មិនទាន់បើក Public Link';
        qrImg.src = networkData.qr_code_url;
        notice.textContent = '⚡ ចុចប៊ូតុងខាងក្រោមដើម្បីបង្កើត Public HTTPS Link សម្រាប់ប្រើតាម 4G/5G';
        btnTunnel.style.display = 'inline-flex';
      }
    } else {
      urlInput.value = networkData.local_url;
      qrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=${networkData.local_url}`;
      notice.textContent = '🏠 ក្នុង Wi-Fi ផ្ទះ: ទូរស័ព្ទ និងកុំព្យូទ័រត្រូវភ្ជាប់ Wi-Fi តែមួយ';
      btnTunnel.style.display = 'none';
    }
  }

  btnOpen?.addEventListener('click', () => {
    modal.style.display = 'flex';
    refreshNetworkInfo();
  });

  btnClose?.addEventListener('click', () => {
    modal.style.display = 'none';
  });

  tabPublic?.addEventListener('click', () => {
    tabPublic.classList.add('active');
    tabLocal.classList.remove('active');
    currentMode = 'public';
    updateModalDisplay();
  });

  tabLocal?.addEventListener('click', () => {
    tabLocal.classList.add('active');
    tabPublic.classList.remove('active');
    currentMode = 'local';
    updateModalDisplay();
  });

  btnTunnel?.addEventListener('click', async () => {
    btnTunnel.disabled = true;
    btnTunnel.innerHTML = `<span class="spinner"></span> កំពុងបង្កើត Cloudflare Tunnel...`;
    showToast('កំពុងបង្កើត Public HTTPS Link...', 'info');

    try {
      const res = await fetch('/api/tunnel/start', { method: 'POST' });
      const data = await res.json();
      if (data.success && data.public_url) {
        showToast('🎉 បង្កើត Public Link ជោគជ័យ!', 'success');
        await refreshNetworkInfo();
      } else {
        showToast(data.error || 'បរាជ័យក្នុងការបង្កើត Tunnel', 'error');
      }
    } catch (err) {
      showToast('Error: ' + err.message, 'error');
    } finally {
      btnTunnel.disabled = false;
      btnTunnel.innerHTML = `<span>⚡</span> បង្កើត Public HTTPS Link ថ្មី`;
    }
  });

  btnCopy?.addEventListener('click', () => {
    if (urlInput && urlInput.value && !urlInput.value.includes('មិនទាន់')) {
      navigator.clipboard.writeText(urlInput.value).then(() => {
        showToast('📋 បាន Copy Link រួចរាល់!', 'success');
      }).catch(() => {
        urlInput.select();
        document.execCommand('copy');
        showToast('📋 បាន Copy Link រួចរាល់!', 'success');
      });
    }
  });
}
