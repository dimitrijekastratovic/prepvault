import { useEffect, useState } from 'react'
import './App.css'
import Editor from './components/Editor'
import Header from './components/Header'
import ProblemPanel from './components/ProblemPanel'

function App() {
  const [currentProblem, setCurrentProblem] = useState(null)
  const [problems, setProblems] = useState([])
  const [isDark, setIsDark] = useState(false)

  useEffect(() => {
    fetch("/api/problems").then(res => res.json())
    .then(data => setProblems(data))
    .catch(err => console.error(err))
  }, [])

  function selectProblem(id) {
    fetch(`/api/problems/${id}`)
      .then(res => res.json())
      .then(data => setCurrentProblem(data))
      .catch(err => console.error(err))
}

  return (
    <div className="playground">
      <Header isDark={isDark} setIsDark={setIsDark} />
      {currentProblem === null ? (
        <div className="problems-list">
          <h1>Problems</h1>
          <ul>
            {problems.map(problem => (
              <li key={problem.id} onClick={() => selectProblem(problem.id)}>
                {problem.title}
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <>
          <div className="playground-toolbar">
            <button onClick={() => setCurrentProblem(null)}>← Back</button>
          </div>
          <div className="playground-body">
            <ProblemPanel problem={currentProblem} />
            <Editor problem={currentProblem} isDark={isDark} />
          </div>
        </>
      )}
    </div>
  )
}

export default App
