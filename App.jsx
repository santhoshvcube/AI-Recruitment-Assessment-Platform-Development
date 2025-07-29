import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { 
  Brain, 
  FileText, 
  MessageSquare, 
  BarChart3, 
  Shield, 
  Users, 
  Upload, 
  CheckCircle,
  ArrowRight,
  Star,
  Clock,
  Target
} from 'lucide-react'
import './App.css'

// Import components
import Header from './components/Header'
import Hero from './components/Hero'
import Features from './components/Features'
import HowItWorks from './components/HowItWorks'
import Dashboard from './components/Dashboard'
import UploadResume from './components/UploadResume'
import Interview from './components/Interview'
import Reports from './components/Reports'
import Footer from './components/Footer'
import LoginPage from './components/LoginPage'
import ChangePassword from './components/ChangePassword'
import StudentDashboard from './components/StudentDashboard'

function App() {
  const [currentUser, setCurrentUser] = useState(null)

  // Check if user is authenticated
  const isAuthenticated = () => {
    return localStorage.getItem('authToken') !== null;
  };

  // Check user type
  const getUserType = () => {
    const userData = localStorage.getItem('userData');
    if (userData) {
      return JSON.parse(userData).userType;
    }
    return null;
  };

  // Check if it's first login for student
  const isFirstLogin = () => {
    const userData = localStorage.getItem('userData');
    if (userData) {
      return JSON.parse(userData).firstLogin;
    }
    return false;
  };

  // Protected Route Component
  const ProtectedRoute = ({ children, requiredUserType = null }) => {
    if (!isAuthenticated()) {
      return <Navigate to="/login" replace />;
    }

    const userType = getUserType();
    if (requiredUserType && userType !== requiredUserType) {
      return <Navigate to="/login" replace />;
    }

    // Redirect student to change password if first login
    if (userType === 'student' && isFirstLogin() && window.location.pathname !== '/change-password') {
      return <Navigate to="/change-password" replace />;
    }

    return children;
  };

  // Landing Page Component
  const LandingPage = () => (
    <main>
      <Hero />
      <Features />
      <HowItWorks />
    </main>
  );

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={
            <>
              <Header currentUser={currentUser} setCurrentUser={setCurrentUser} />
              <LandingPage />
              <Footer />
            </>
          } />
          
          <Route path="/login" element={
            isAuthenticated() ? (
              getUserType() === 'student' ? (
                isFirstLogin() ? <Navigate to="/change-password" replace /> : <Navigate to="/student-dashboard" replace />
              ) : (
                <Navigate to="/dashboard" replace />
              )
            ) : (
              <LoginPage />
            )
          } />

          {/* Student Routes */}
          <Route path="/change-password" element={
            <ProtectedRoute requiredUserType="student">
              <ChangePassword />
            </ProtectedRoute>
          } />
          
          <Route path="/student-dashboard" element={
            <ProtectedRoute requiredUserType="student">
              <StudentDashboard />
            </ProtectedRoute>
          } />

          <Route path="/trial-dashboard" element={
            <ProtectedRoute requiredUserType="trial">
              <TrialDashboard />
            </ProtectedRoute>
          } />

          {/* Admin Routes */}
          <Route path="/dashboard" element={
            <ProtectedRoute requiredUserType="admin">
              <>
                <Header currentUser={currentUser} setCurrentUser={setCurrentUser} />
                <Dashboard currentUser={currentUser} />
                <Footer />
              </>
            </ProtectedRoute>
          } />
          
          <Route path="/upload" element={
            <ProtectedRoute requiredUserType="admin">
              <>
                <Header currentUser={currentUser} setCurrentUser={setCurrentUser} />
                <UploadResume currentUser={currentUser} />
                <Footer />
              </>
            </ProtectedRoute>
          } />
          
          <Route path="/interview/:sessionId" element={
            <ProtectedRoute>
              <>
                <Header currentUser={currentUser} setCurrentUser={setCurrentUser} />
                <Interview currentUser={currentUser} />
                <Footer />
              </>
            </ProtectedRoute>
          } />
          
          <Route path="/reports" element={
            <ProtectedRoute>
              <>
                <Header currentUser={currentUser} setCurrentUser={setCurrentUser} />
                <Reports currentUser={currentUser} />
                <Footer />
              </>
            </ProtectedRoute>
          } />

          {/* Fallback Route */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App


import TrialDashboard from './components/TrialDashboard';

