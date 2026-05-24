function ProblemPanel({ problem }) {
  return (
    <div className="problem-panel">
      <h2>{problem.title}</h2>
      <span className={`difficulty ${problem.difficulty.toLowerCase()}`}>
        {problem.difficulty}
      </span>
      <p>{problem.description}</p>
      <h3>Constraints</h3>
      <div className="constraints">{problem.constraints}</div>
      <h3>Topics</h3>
      <ul className="topics">
        {problem.topics.map((topic) => (
          <li key={topic}>{topic}</li>
        ))}
      </ul>
    </div>
  )
}

export default ProblemPanel
