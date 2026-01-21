const { createFFmpeg, fetchFile } = FFmpeg;
const ffmpeg = createFFmpeg({ log: true });

const videoInput = document.getElementById("videoInput");
const extractBtn = document.getElementById("extractBtn");
const statusText = document.getElementById("status");
const downloadLink = document.getElementById("downloadLink");

extractBtn.onclick = async () => {
  if (!videoInput.files.length) {
    alert("Please select a video file");
    return;
  }

  const videoFile = videoInput.files[0];

  statusText.textContent = "Loading FFmpeg...";
  if (!ffmpeg.isLoaded()) {
    await ffmpeg.load();
  }

  statusText.textContent = "Processing video...";

  ffmpeg.FS("writeFile", "input.mp4", await fetchFile(videoFile));

  await ffmpeg.run(
    "-i", "input.mp4",
    "-q:a", "0",
    "-map", "a",
    "output.mp3"
  );

  const data = ffmpeg.FS("readFile", "output.mp3");
  const audioBlob = new Blob([data.buffer], { type: "audio/mp3" });
  const audioUrl = URL.createObjectURL(audioBlob);

  downloadLink.href = audioUrl;
  downloadLink.style.display = "block";
  statusText.textContent = "Done";
};
