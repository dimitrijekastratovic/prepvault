import { useEffect } from 'react'

function Header({ isDark, setIsDark }) {
  useEffect(() => {
    const saved = localStorage.getItem('theme')
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    const dark = saved ? saved === 'dark' : prefersDark
    setIsDark(dark)
    document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light')
  }, [])

  function toggleTheme() {
    const next = !isDark
    setIsDark(next)
    localStorage.setItem('theme', next ? 'dark' : 'light')
    document.documentElement.setAttribute('data-theme', next ? 'dark' : 'light')
  }

  function logout() {
    fetch('/auth/logout', { method: 'POST' })
      .then(() => { window.location.href = '/' })
      .catch(() => { window.location.href = '/' })
  }

  return (
    <header className="header">
      <div className="header-side" />
      <a href="/" className="header-logo">PrepVault</a>
      <div className="header-side header-actions">
        <button className="header-btn" onClick={toggleTheme} aria-label="Toggle theme">
          {isDark ? '☀️' : '🌙'}
        </button>
        <button className="header-btn" onClick={logout}>Logout</button>
      </div>
    </header>
  )
}

export default Header
