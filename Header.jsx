import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  Brain, 
  Menu, 
  X, 
  User, 
  LogOut, 
  Settings,
  BarChart3,
  Upload,
  FileText
} from 'lucide-react'

const Header = ({ currentUser, setCurrentUser }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const navigate = useNavigate()

  const handleLogin = () => {
    navigate('/login')
  }

  const handleLogout = () => {
    setCurrentUser(null)
    navigate('/')
  }

  return (
    <header className="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-2 rounded-lg">
              <Brain className="h-6 w-6 text-white" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              AI Interview
            </span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {currentUser ? (
              <>
                <Link 
                  to="/dashboard" 
                  className="flex items-center space-x-1 text-slate-600 hover:text-blue-600 transition-colors"
                >
                  <BarChart3 className="h-4 w-4" />
                  <span>Dashboard</span>
                </Link>
                <Link 
                  to="/upload" 
                  className="flex items-center space-x-1 text-slate-600 hover:text-blue-600 transition-colors"
                >
                  <Upload className="h-4 w-4" />
                  <span>Upload Resume</span>
                </Link>
                <Link 
                  to="/reports" 
                  className="flex items-center space-x-1 text-slate-600 hover:text-blue-600 transition-colors"
                >
                  <FileText className="h-4 w-4" />
                  <span>Reports</span>
                </Link>
              </>
            ) : (
              <>
                <a href="#features" className="text-slate-600 hover:text-blue-600 transition-colors">
                  Features
                </a>
                <a href="#how-it-works" className="text-slate-600 hover:text-blue-600 transition-colors">
                  How It Works
                </a>
                <a href="#pricing" className="text-slate-600 hover:text-blue-600 transition-colors">
                  Pricing
                </a>
              </>
            )}
          </nav>

          {/* User Actions */}
          <div className="hidden md:flex items-center space-x-4">
            {currentUser ? (
              <div className="flex items-center space-x-3">
                <Badge variant="secondary" className="bg-blue-100 text-blue-700">
                  {currentUser.role}
                </Badge>
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
                    <User className="h-4 w-4 text-white" />
                  </div>
                  <span className="text-sm font-medium text-slate-700">{currentUser.name}</span>
                </div>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  onClick={handleLogout}
                  className="text-slate-600 hover:text-red-600"
                >
                  <LogOut className="h-4 w-4" />
                </Button>
              </div>
            ) : (
              <div className="flex items-center space-x-3">
                <Button variant="ghost" onClick={handleLogin}>
                  Sign In
                </Button>
                <Button onClick={handleLogin} className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                  Get Started
                </Button>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-slate-200">
            <div className="flex flex-col space-y-3">
              {currentUser ? (
                <>
                  <Link 
                    to="/dashboard" 
                    className="flex items-center space-x-2 text-slate-600 hover:text-blue-600 transition-colors py-2"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    <BarChart3 className="h-4 w-4" />
                    <span>Dashboard</span>
                  </Link>
                  <Link 
                    to="/upload" 
                    className="flex items-center space-x-2 text-slate-600 hover:text-blue-600 transition-colors py-2"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    <Upload className="h-4 w-4" />
                    <span>Upload Resume</span>
                  </Link>
                  <Link 
                    to="/reports" 
                    className="flex items-center space-x-2 text-slate-600 hover:text-blue-600 transition-colors py-2"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    <FileText className="h-4 w-4" />
                    <span>Reports</span>
                  </Link>
                  <div className="flex items-center justify-between pt-3 border-t border-slate-200">
                    <div className="flex items-center space-x-2">
                      <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
                        <User className="h-4 w-4 text-white" />
                      </div>
                      <span className="text-sm font-medium text-slate-700">{currentUser.name}</span>
                    </div>
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      onClick={handleLogout}
                      className="text-slate-600 hover:text-red-600"
                    >
                      <LogOut className="h-4 w-4" />
                    </Button>
                  </div>
                </>
              ) : (
                <>
                  <a 
                    href="#features" 
                    className="text-slate-600 hover:text-blue-600 transition-colors py-2"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    Features
                  </a>
                  <a 
                    href="#how-it-works" 
                    className="text-slate-600 hover:text-blue-600 transition-colors py-2"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    How It Works
                  </a>
                  <a 
                    href="#pricing" 
                    className="text-slate-600 hover:text-blue-600 transition-colors py-2"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    Pricing
                  </a>
                  <div className="pt-3 border-t border-slate-200">
                    <Button 
                      onClick={handleLogin} 
                      className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                    >
                      Get Started
                    </Button>
                  </div>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </header>
  )
}

export default Header

