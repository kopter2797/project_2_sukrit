document.addEventListener("DOMContentLoaded", () => {
  // Buttons
  const actionBtns = document.querySelectorAll(".action-btn");
  const mainActionBtn = document.getElementById("mainActionBtn");
  const mainActionText = document.getElementById("mainActionText");
  const mainActionIcon = document.getElementById("mainActionIcon");
  const cipherBtns = document.querySelectorAll(".cipher-btn");

  // Inputs
  const keyGroup = document.getElementById("keyGroup");
  const inputKey = document.getElementById("inputKey");
  const inputKeyMulti = document.getElementById("inputKeyMulti");
  const inputText = document.getElementById("inputText");
  const outputText = document.getElementById("outputText");
  const copyBtn = document.getElementById("copyBtn");

  // State
  let currentCipher = "vigenere";
  let currentAction = "encrypt"; // Default action

  // --- Segmented Control Logic ---
  function updateSegmentIndicator(
    containerSelector,
    indicatorSelector,
    activeBtn,
  ) {
    if (!activeBtn) return;
    const indicator = document.querySelector(indicatorSelector);
    if (!indicator) return;

    const left = activeBtn.offsetLeft;
    const width = activeBtn.offsetWidth;

    indicator.style.width = `${width}px`;
    indicator.style.transform = `translateX(${left - 8}px)`;
  }

  // --- Cipher Selector Events ---
  cipherBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      cipherBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      currentCipher = btn.dataset.cipher;

      updateSegmentIndicator(".segmented-control", ".active-indicator", btn);
      updateUI(currentCipher);
    });
  });

  // --- Action Selector Events ---
  actionBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      actionBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      currentAction = btn.dataset.action;

      updateSegmentIndicator(
        ".action-selector",
        ".active-indicator-action",
        btn,
      );
      updateActionUI();
    });
  });

  // --- Initial Layout Update ---
  function initialLayout() {
    const activeCipherBtn = document.querySelector(".cipher-btn.active");
    const activeActionBtn = document.querySelector(".action-btn.active");

    if (activeCipherBtn)
      updateSegmentIndicator(
        ".segmented-control",
        ".active-indicator",
        activeCipherBtn,
      );
    if (activeActionBtn)
      updateSegmentIndicator(
        ".action-selector",
        ".active-indicator-action",
        activeActionBtn,
      );
  }

  setTimeout(initialLayout, 100);
  window.addEventListener("resize", initialLayout);

  // --- UI Update Helper ---
  function updateUI(cipher) {
    keyGroup.style.display = "block";

    if (cipher === "caesar") {
      inputKey.placeholder = "กรอกจำนวนการเลื่อน (เช่น 3)";
      inputKey.type = "number";
    } else if (cipher === "number") {
      inputKey.placeholder = "กรอกตัวเลขคีย์ (เช่น 5)";
      inputKey.type = "number";
    } else {
      inputKey.placeholder = "กรอกคีย์ (เช่น SECRET)";
      inputKey.type = "text";
    }
  }

  function updateActionUI() {
    if (currentAction === "encrypt") {
      mainActionText.innerText = "RUN ENCRYPT";
      mainActionIcon.className = "ph-bold ph-lock-key text-xl";
      inputKey.classList.remove("hidden");
      inputKeyMulti.classList.add("hidden");
    } else if (currentAction === "decrypt") {
      mainActionText.innerText = "RUN DECRYPT";
      mainActionIcon.className = "ph-bold ph-lock-key-open text-xl";
      inputKey.classList.remove("hidden");
      inputKeyMulti.classList.add("hidden");
    } else if (currentAction === "autocrack") {
      mainActionText.innerText = "RUN AUTO CRACK";
      mainActionIcon.className = "ph-bold ph-magic-wand text-xl";
      inputKey.classList.add("hidden");
      inputKeyMulti.classList.remove("hidden");
    }
  }

  // --- API Process ---
  async function processCipher(action) {
    const text = inputText.value;
    let key; 
    
    if (action === "autocrack") {
        key = inputKeyMulti.value;
    } else {
        key = inputKey.value;
    }

    if (!text) {
      alert("กรุณากรอกข้อความ");
      return;
    }

    if (!key) {
      if (action === "autocrack") {
         alert("กรุณากรอกคีย์อย่างน้อย 1 ตัว");
      } else {
         alert("กรุณากรอกคีย์");
      }
      return;
    }

    const startTime = Date.now();

    // Loading State
    const originalText = mainActionText.innerText;
    mainActionText.innerText = "PROCESSING...";
    mainActionBtn.disabled = true;

    try {
      const response = await fetch("/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: currentCipher,
          action: action,
          text: text,
          key: key,
        }),
      });

      console.log("Response received");
      const data = await response.json();
      const finalTime = data.time ? data.time : (Date.now() - startTime) / 1000;

      outputText.innerText = data.result;
      addLog(action, currentCipher, finalTime);

      // Success Feedback
      mainActionText.innerText = "SUCCESS!";
      setTimeout(() => {
        updateActionUI();
        mainActionBtn.disabled = false;
      }, 1000);
    } catch (error) {
      console.error("Error:", error);
      outputText.innerText = "เกิดข้อผิดพลาด";
      mainActionText.innerText = "ERROR";
      setTimeout(() => {
        updateActionUI();
        mainActionBtn.disabled = false;
      }, 1000);
    }
  }

  mainActionBtn.addEventListener("click", () => processCipher(currentAction));

  // --- Copy Functionality ---
  copyBtn.addEventListener("click", () => {
    // Modern Clipboard API with Fallback
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard
        .writeText(outputText.innerText)
        .then(showCopySuccess)
        .catch((err) => {
          console.error("Async copy failed", err);
          fallbackCopy();
        });
    } else {
      fallbackCopy();
    }
  });

  function showCopySuccess() {
    const originalIcon = copyBtn.innerHTML;
    copyBtn.innerHTML = '<i class="ph-bold ph-check text-green-400"></i>';
    setTimeout(() => (copyBtn.innerHTML = originalIcon), 2000);
  }

  function fallbackCopy() {
    const range = document.createRange();
    range.selectNodeContents(outputText);
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    try {
      const successful = document.execCommand("copy");
      if (successful) showCopySuccess();
      else console.error("Fallback copy unsuccessful");
    } catch (e) {
      console.error("Fallback failed", e);
    }
    selection.removeAllRanges();
  }

  // --- Log Console ---
  const logConsole = document.getElementById("logConsole");
  const clearLogBtn = document.getElementById("clearLogBtn");

  function addLog(action, cipher, time) {
    if (!logConsole) return;
    const now = new Date();
    const timeString = now.toLocaleTimeString("en-US", { hour12: false });
    const entry = document.createElement("div");

    entry.className = "log-entry success";
    entry.innerHTML = `<span class="log-timestamp">[${timeString}]</span> ${action.toUpperCase()} (${cipher}): ${time.toFixed(6)}s`;

    logConsole.appendChild(entry);
    logConsole.scrollTop = logConsole.scrollHeight;
  }

  if (clearLogBtn) {
    clearLogBtn.addEventListener("click", () => {
      logConsole.innerHTML =
        '<div class="log-entry system">> Console cleared...</div>';
    });
  }

  // Initial UI Setup Call
  updateUI(currentCipher);
});
