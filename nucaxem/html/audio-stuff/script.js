const { createFFmpeg, fetchFile } = FFmpeg;

const ffmpeg = createFFmpeg({
  log: true,
  progress: ({ ratio }) => {
    const percent = Math.round(ratio * 100);
    progressBar.style.width = percent + "%";
    statusText.textContent = `Processing: ${percent}%`;
  }
});

const videoInput = document.getElementById("videoInput");
const extractBtn = document.getElementById("extractBtn");
const progressBar = document.getElementById("progressBar");
const statusText = document.getElementById("status");
const downloadLink = document.getElementById("downloadLink");

extractBtn.onclick = async () => {
  if (!videoInput.files.length) {
    alert("Please select a video file");
    return;
  }

  progressBar.style.width = "0%";
  downloadLink.style.display = "none";
  statusText.textContent = "Loading FFmpeg...";

  if (!ffmpeg.isLoaded()) {
    await ffmpeg.load();
  }

  const file = videoInput.files[0];

  statusText.textContent = "Reading video...";
  ffmpeg.FS("writeFile", "input.mp4", await fetchFile(file));

  statusText.textContent = "Extracting audio...";
  await ffmpeg.run(
    "-i", "input.mp4",
    "-vn",
    "-acodec", "libmp3lame",
    "-ab", "192k",
    "output.mp3"
  );

  const data = ffmpeg.FS("readFile", "output.mp3");
  const audioBlob = new Blob([data.buffer], { type: "audio/mp3" });
  const audioURL = URL.createObjectURL(audioBlob);

  downloadLink.href = audioURL;
  downloadLink.style.display = "block";
  statusText.textContent = "Done";
};
