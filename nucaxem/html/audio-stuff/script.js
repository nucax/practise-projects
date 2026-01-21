const { createFFmpeg, fetchFile } = FFmpeg;

const progressBar = document.getElementById("progressBar");
const statusText = document.getElementById("status");

const ffmpeg = createFFmpeg({
  log: true,
  progress: ({ ratio }) => {
    if (!ratio) return;
    const percent = Math.min(100, Math.round(ratio * 100));
    progressBar.style.width = percent + "%";
    statusText.textContent = `Processing: ${percent}%`;
  }
});

const videoInput = document.getElementById("videoInput");
const extractBtn = document.getElementById("extractBtn");
const downloadLink = document.getElementById("downloadLink");

extractBtn.onclick = async () => {
  if (!videoInput.files.length) {
    alert("Select a video first");
    return;
  }

  try {
    progressBar.style.width = "5%";
    downloadLink.style.display = "none";
    statusText.textContent = "Loading FFmpeg...";

    if (!ffmpeg.isLoaded()) {
      await ffmpeg.load();
    }

    const file = videoInput.files[0];
    const ext = file.name.split(".").pop(); // mov, mp4, etc
    const inputName = `input.${ext}`;

    statusText.textContent = "Reading file...";
    progressBar.style.width = "15%";

    ffmpeg.FS("writeFile", inputName, await fetchFile(file));

    statusText.textContent = "Extracting audio...";
    progressBar.style.width = "25%";

    await ffmpeg.run(
      "-i", inputName,
      "-vn",
      "-acodec", "mp3",
      "-ab", "192k",
      "output.mp3"
    );

    const data = ffmpeg.FS("readFile", "output.mp3");
    const audioBlob = new Blob([data.buffer], { type: "audio/mp3" });
    const audioURL = URL.createObjectURL(audioBlob);

    downloadLink.href = audioURL;
    downloadLink.style.display = "block";

    progressBar.style.width = "100%";
    statusText.textContent = "Done";
  } catch (err) {
    console.error(err);
    statusText.textContent = "Error: unsupported file or browser";
  }
};
