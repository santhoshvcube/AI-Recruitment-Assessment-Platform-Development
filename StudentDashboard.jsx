import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  User, 
  FileText, 
  Clock, 
  CheckCircle, 
  AlertCircle, 
  BookOpen, 
  Calendar,
  Award,
  TrendingUp,
  LogOut
} from 'lucide-react';

const StudentDashboard = () => {
  const [userData, setUserData] = useState(null);
  const [assessments, setAssessments] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // Load user data from localStorage (in real app, fetch from API)
    const storedUserData = localStorage.getItem('userData');
    if (storedUserData) {
      setUserData(JSON.parse(storedUserData));
    }

    // Mock assessments data
    setAssessments([
      {
        id: 1,
        jobTitle: 'Frontend Developer',
        company: 'TechCorp',
        status: 'completed',
        score: 85,
        completedAt: '2024-01-20',
        duration: 45,
        recommendation: 'hire'
      },
      {
        id: 2,
        jobTitle: 'React Developer',
        company: 'StartupXYZ',
        status: 'in_progress',
        score: null,
        startedAt: '2024-01-22',
        duration: null,
        recommendation: null
      },
      {
        id: 3,
        jobTitle: 'Full Stack Developer',
        company: 'InnovateLab',
        status: 'scheduled',
        score: null,
        scheduledAt: '2024-01-25',
        duration: null,
        recommendation: null
      }
    ]);

    setLoading(false);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userData');
    navigate('/login');
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'in_progress':
        return <Clock className="w-5 h-5 text-blue-500" />;
      case 'scheduled':
        return <Calendar className="w-5 h-5 text-orange-500" />;
      default:
        return <AlertCircle className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'completed':
        return 'Completed';
      case 'in_progress':
        return 'In Progress';
      case 'scheduled':
        return 'Scheduled';
      default:
        return 'Unknown';
    }
  };

  const getRecommendationBadge = (recommendation) => {
    switch (recommendation) {
      case 'strong_hire':
        return <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">Strong Hire</span>;
      case 'hire':
        return <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">Hire</span>;
      case 'maybe':
        return <span className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs font-medium rounded-full">Maybe</span>;
      case 'no_hire':
        return <span className="px-2 py-1 bg-red-100 text-red-800 text-xs font-medium rounded-full">No Hire</span>;
      default:
        return null;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  const completedAssessments = assessments.filter(a => a.status === 'completed');
  const averageScore = completedAssessments.length > 0 
    ? Math.round(completedAssessments.reduce((sum, a) => sum + a.score, 0) / completedAssessments.length)
    : 0;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center mr-3">
                <span className="text-white font-bold text-sm">AI</span>
              </div>
              <h1 className="text-xl font-semibold text-gray-900">Student Portal</h1>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center text-sm text-gray-600">
                <User className="w-4 h-4 mr-2" />
                {userData?.email}
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center text-sm text-gray-600 hover:text-gray-900 transition-colors"
              >
                <LogOut className="w-4 h-4 mr-1" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Welcome back, Student!
          </h2>
          <p className="text-gray-600">
            Track your assessment progress and view your results.
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <FileText className="w-6 h-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Assessments</p>
                <p className="text-2xl font-bold text-gray-900">{assessments.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <CheckCircle className="w-6 h-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Completed</p>
                <p className="text-2xl font-bold text-gray-900">{completedAssessments.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Award className="w-6 h-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Average Score</p>
                <p className="text-2xl font-bold text-gray-900">{averageScore}%</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-orange-100 rounded-lg">
                <TrendingUp className="w-6 h-6 text-orange-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">In Progress</p>
                <p className="text-2xl font-bold text-gray-900">
                  {assessments.filter(a => a.status === 'in_progress').length}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Assessments List */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">My Assessments</h3>
          </div>
          <div className="divide-y divide-gray-200">
            {assessments.map((assessment) => (
              <div key={assessment.id} className="px-6 py-4 hover:bg-gray-50 transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center mb-2">
                      {getStatusIcon(assessment.status)}
                      <h4 className="ml-2 text-lg font-medium text-gray-900">
                        {assessment.jobTitle}
                      </h4>
                      <span className="ml-2 text-sm text-gray-500">at {assessment.company}</span>
                    </div>
                    <div className="flex items-center space-x-4 text-sm text-gray-600">
                      <span className="flex items-center">
                        <Calendar className="w-4 h-4 mr-1" />
                        {assessment.status === 'completed' && `Completed on ${assessment.completedAt}`}
                        {assessment.status === 'in_progress' && `Started on ${assessment.startedAt}`}
                        {assessment.status === 'scheduled' && `Scheduled for ${assessment.scheduledAt}`}
                      </span>
                      {assessment.duration && (
                        <span className="flex items-center">
                          <Clock className="w-4 h-4 mr-1" />
                          {assessment.duration} minutes
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center space-x-4">
                    {assessment.score && (
                      <div className="text-right">
                        <p className="text-2xl font-bold text-gray-900">{assessment.score}%</p>
                        <p className="text-sm text-gray-500">Score</p>
                      </div>
                    )}
                    {assessment.recommendation && getRecommendationBadge(assessment.recommendation)}
                    <div className="flex flex-col space-y-2">
                      {assessment.status === 'completed' && (
                        <button className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors">
                          View Report
                        </button>
                      )}
                      {assessment.status === 'in_progress' && (
                        <button className="px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-lg hover:bg-green-700 transition-colors">
                          Continue
                        </button>
                      )}
                      {assessment.status === 'scheduled' && (
                        <button className="px-4 py-2 bg-orange-600 text-white text-sm font-medium rounded-lg hover:bg-orange-700 transition-colors">
                          Start Assessment
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center mb-4">
              <BookOpen className="w-6 h-6 text-blue-600 mr-3" />
              <h3 className="text-lg font-medium text-gray-900">Preparation Resources</h3>
            </div>
            <p className="text-gray-600 mb-4">
              Access study materials and practice questions to improve your assessment performance.
            </p>
            <button className="w-full px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors">
              View Resources
            </button>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center mb-4">
              <User className="w-6 h-6 text-purple-600 mr-3" />
              <h3 className="text-lg font-medium text-gray-900">Profile Settings</h3>
            </div>
            <p className="text-gray-600 mb-4">
              Update your personal information and preferences.
            </p>
            <button className="w-full px-4 py-2 bg-purple-600 text-white font-medium rounded-lg hover:bg-purple-700 transition-colors">
              Edit Profile
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentDashboard;

