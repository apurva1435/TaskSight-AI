import { useEffect, useState } from "react"
import axios from "axios"

function App() {

  const [image, setImage] = useState(null)
  const [preview, setPreview] = useState(null)
  const [darkMode, setDarkMode] = useState(false)

  const [result, setResult] = useState(null)

  const [history, setHistory] = useState([])

  const [loading, setLoading] = useState(false)

  const [isDrawing, setIsDrawing] = useState(false)

  const [startPoint, setStartPoint] = useState(null)

  const [selectionBox, setSelectionBox] = useState(null)

  const fetchHistory = async () => {

    try {


      const response = await axios.get(
        "http://127.0.0.1:8000/history"
      )

      setHistory(response.data.experiments)

    } catch (error) {

      console.log(error)
    }
  }

  useEffect(() => {

    fetchHistory()

  }, [])

const analyzeImage = async () => {

  if (!image) {

    alert("Please upload an image")
    return
  }

  if (!selectionBox) {

    alert("Please select a human attention region")
    return
  }

  console.log("SELECTION BOX")
  console.log(selectionBox)

  const formData = new FormData()

  formData.append("file", image)

  formData.append(
    "human_x",
    selectionBox.x
  )

  formData.append(
    "human_y",
    selectionBox.y
  )

  formData.append(
    "human_width",
    selectionBox.width
  )

  formData.append(
    "human_height",
    selectionBox.height
  )

const img = document.querySelector(
  ".preview-image"
)

formData.append(
  "display_width",
  img.clientWidth
)

formData.append(
  "display_height",
  img.clientHeight
)

  try {

    setLoading(true)

    const response = await axios.post(
      "http://127.0.0.1:8000/compare",
      formData
    )

    setResult(response.data)

    fetchHistory()

  } catch (error) {

    console.log(error)

    alert("Error connecting to backend")

  } finally {

    setLoading(false)
  }
}

  const handleImageUpload = (e) => {

    const file = e.target.files[0]

    setImage(file)

    setPreview(URL.createObjectURL(file))

    setSelectionBox(null)

    setResult(null)
  }

  const handleMouseDown = (e) => {

    const rect = e.target.getBoundingClientRect()

    const x = e.clientX - rect.left

    const y = e.clientY - rect.top

    setStartPoint({ x, y })

    setIsDrawing(true)
  }

  const handleMouseMove = (e) => {

    if (!isDrawing || !startPoint) return

    const rect = e.target.getBoundingClientRect()

    const currentX = e.clientX - rect.left

    const currentY = e.clientY - rect.top

    const x = Math.min(startPoint.x, currentX)

    const y = Math.min(startPoint.y, currentY)

    const width = Math.abs(currentX - startPoint.x)

    const height = Math.abs(currentY - startPoint.y)

    setSelectionBox({
      x,
      y,
      width,
      height
    })
  }

  const handleMouseUp = () => {

    setIsDrawing(false)
  }

  return (

    <div className={`container ${darkMode ? "dark" : ""}`}>

<div className="hero-section">

  

  <h1>
    TaskSight AI
  </h1>

  <p>
    Human vs AI Attention Analysis Platform
  </p>

</div>

<button
  onClick={() => setDarkMode(!darkMode)}
  style={{
    marginBottom: "20px"
  }}
>
  {darkMode ? "☀ Light Mode" : "🌙 Dark Mode"}
</button>

      <div className="section">

        <label>Upload Image</label>

        <input
          type="file"
          onChange={handleImageUpload}
        />

      </div>

      {preview && (

        <div className="preview-box">

          <h3>
            Human Task:
            Drag around the object you focus on
          </h3>

          <div
            style={{
              position: "relative",
              display: "inline-block"
            }}
          >

            <img
              src={preview}
              alt="Preview"
              className="preview-image"
              onMouseDown={handleMouseDown}
              onMouseMove={handleMouseMove}
              onMouseUp={handleMouseUp}
            />

            {selectionBox && (

              <div
                style={{
                  position: "absolute",
                  left: selectionBox.x,
                  top: selectionBox.y,
                  width: selectionBox.width,
                  height: selectionBox.height,
                  border: "3px solid red",
                  pointerEvents: "none"
                }}
              />

            )}

          </div>

        </div>

      )}

      <button
        onClick={analyzeImage}
        disabled={loading}
      >

        {loading
          ? "Running Full Experiment..."
          : "Run Full Experiment"}

      </button>

      {result && (

        <div className="result-card">

          <h2>
            ActiveVision Comparison
          </h2>

          <div className="comparison-grid">

            <div className="comparison-card">

              <h3>
                Human Attention
              </h3>

              <img
                src={preview}
                alt="Human"
                className="comparison-image"
              />

            </div>

            <div className="comparison-card">

  <h3>
    AI Attention
  </h3>

  <img
    src={`http://127.0.0.1:8000/outputs/${result.attention_map}`}
    alt="Attention"
    className="comparison-image"
  />

</div>

<div className="comparison-card">

  <h3>
    YOLO Object Detection
  </h3>

  <img
    src={`http://127.0.0.1:8000/outputs/${result.yolo_visualization}`}
    alt="YOLO"
    className="comparison-image"
  />

</div>

<div className="output-box">

  <h3>
    Human vs AI Overlay
  </h3>

  <img
    src={`http://127.0.0.1:8000/outputs/${result.overlay_visualization}`}
    alt="Overlay"
    className="comparison-image"
  />

  <p>

    🟥 Red = Human Selection

    <br />

    🟩 Green = AI Detection

  </p>

</div>

          </div>

          <div className="score-card">

            <button

  onClick={() => {

    const report = `

TaskSight AI Report

Caption: ${result.caption}

Selected Object: ${result.human_selected_object}

Agreement Score: ${result.agreement_score}%

`

    const blob = new Blob(
      [report],
      { type: "text/plain" }
    )

    const url =
      URL.createObjectURL(blob)

    const a =
      document.createElement("a")

    a.href = url

    a.download =
      "tasksight_report.txt"

    a.click()

  }}

>

  ⬇ Download Report

</button>

            <h3>
              Attention Agreement Score
            </h3>

            <h2>
              {result.agreement_score}%
            </h2>

          </div>

          <div className="output-box">

  <h3>
    Human Selected Object
  </h3>

  <p>
    {result.human_selected_object}
  </p>

</div>

<div className="output-box">

  <h3>
    Human-AI Attention Agreement
  </h3>

  {

    result.human_selected_object !== "No Match"

    ? (

      <p
        style={{
          color: "green",
          fontWeight: "bold"
        }}
      >

        MATCH ✅

      </p>

    )

    : (

      <p
        style={{
          color: "red",
          fontWeight: "bold"
        }}
      >

        NO MATCH ❌

      </p>

    )

  }

</div>

          <div className="output-box">

  <h3>
    AI Object Summary
  </h3>

  {
    result?.detected_objects &&

    Object.entries(

      result.detected_objects.reduce(

        (acc, obj) => {

          acc[obj.label] =
            (acc[obj.label] || 0) + 1

          return acc

        },

        {}

      )

    ).map(

      ([label, count]) => (

        <p key={label}>

          ✓ {label} × {count}

        </p>

      )

    )

  }

</div>

          <div className="output-box">

            <h3>Caption</h3>

            <p>{result.caption}</p>

          </div>

          <div className="output-box">

            <h3>Scene Understanding</h3>

            <p>
              {result.task_results.scene_understanding.answer}
            </p>

          </div>

          <div className="output-box">

            <h3>Object Counting</h3>

            <p>
              {result.task_results.object_counting.answer}
            </p>

          </div>

          <div className="output-box">

            <h3>Risk Detection</h3>

            <p>
              {result.task_results.risk_detection.answer}
            </p>

          </div>

          <div className="output-box">

            <h3>Spatial Reasoning</h3>

            <p>
              {result.task_results.spatial_reasoning.answer}
            </p>

          </div>

        </div>

      )}

      <div className="history-section">

        <div className="stats-grid">

  <div className="stat-card">

    <h3>
      Total Experiments
    </h3>

    <h1>
      {history.length}
    </h1>

  </div>

  <div className="stat-card">

    <h3>
      Latest Caption
    </h3>

    <h1>
      {
        history.length > 0
          ? history[0].caption_result
          : "-"
      }
    </h1>

  </div>

</div>

        <h2>
          Experiment History
        </h2>

        {history.map((experiment) => (

          <div
  key={experiment.id}
  className="history-card"
>

  <h3>
    Experiment #{experiment.id}
  </h3>

  <p>
    <strong>Caption:</strong> {experiment.caption_result}
  </p>

  <p>
    <strong>Image:</strong> {experiment.image_name}
  </p>

  <button

    onClick={async () => {

      await axios.delete(

        `http://127.0.0.1:8000/history/${experiment.id}`

      )

      fetchHistory()

    }}

    style={{

      marginTop: "10px",

      background: "#dc2626",

      width: "150px",

      color: "white",

      border: "none",

      padding: "8px 14px",

      borderRadius: "8px",

      cursor: "pointer"

    }}

  >

    🗑 Delete

  </button>

</div>
        ))}

      </div>

    </div>

  )
}

export default App