import MonacoEditor from '@monaco-editor/react'
import { useState } from 'react'

function Editor({ problem, isDark }) {
  const [code, setCode] = useState('')

  return (
    <div className="editor-panel">
      <div className="monaco-wrapper">
        <MonacoEditor
          height="100%"
          language="javascript"
          theme={isDark ? 'vs-dark' : 'light'}
          value={code}
          onChange={setCode}
        />
      </div>
      <div className="editor-toolbar">
        <button onClick={() => console.log(code)}>Submit</button>
      </div>
    </div>
  )
}

export default Editor
