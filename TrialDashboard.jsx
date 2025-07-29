import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  User,
  Clock,
  CheckCircle,
  AlertCircle,
  FileText,
  MessageSquare,
  Award,
  TrendingUp,
  LogOut,
  Timer,
  Play,
  Upload
} from 'lucide-react';

const TrialDashboard = () => {
  const [userData, setUserData] = useState(null);
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const fetchTrialStatus = async () => {
    const authToken = localStorage.getItem('authToken');
    if (!authToken) {
      handleTrialExpired();
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/api/free-trial/status', {
        headers: {
          'Authorization': `Bearer ${authToken}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch trial status');
      }

      const data = await response.json();
      
      if (data.status === 'expired') {
        handleTrialExpired();
        return;
      }

      // Assuming backend returns full_name and email
      const storedUserData = localStorage.getItem('userData');
      let currentUserData = {};
      if (storedUserData) {
        currentUserData = JSON.parse(storedUserData);
      }

      setUserData({
        ...currentUserData,
        email: currentUserData.email, // Assuming email is already in localStorage
        fullName: currentUserData.fullName, // Assuming fullName is already in localStorage
        userType: 'trial',
        trialStartTime: new Date().toISOString(), // This should ideally come from backend
        trialEndTime: new Date(Date.now() + data.time_remaining * 1000).toISOString(),
      });
      setTimeRemaining(data.time_remaining * 1000);

    } catch (error) {
      console.error('Error fetching trial status:', error);
      handleTrialExpired(); // Redirect on error
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTrialStatus();

    const interval = setInterval(() => {
      fetchTrialStatus();
    }, 5000); // Refresh status every 5 seconds

    return () => clearInterval(interval);
  }, []);

  const handleTrialExpired = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userData');
    navigate('/login');
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userData');
    navigate('/login');
  };

  const formatTime = (milliseconds) => {
    const totalSeconds = Math.floor(milliseconds / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const getTimeColor = () => {
    const totalTime = 60 * 60 * 1000; // 1 hour in milliseconds
    const percentage = (timeRemaining / totalTime) * 100;
    
    if (percentage > 50) return 'text-green-600';
    if (percentage > 20) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getProgressColor = () => {
    const totalTime = 60 * 60 * 1000; // 1 hour in milliseconds
    const percentage = (timeRemaining / totalTime) * 100;
    
    if (percentage > 50) return 'bg-green-500';
    if (percentage > 20) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-green-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading trial dashboard...</p>
        </div>
      </div>
    );
  }

  const totalTime = 60 * 60 * 1000; // 1 hour in milliseconds
  const progressPercentage = (timeRemaining / totalTime) * 100;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="w-8 h-8 bg-gradient-to-r from-green-600 to-blue-600 rounded-lg flex items-center justify-center mr-3">
                <span className="text-white font-bold text-sm">AI</span>
              </div>
              <h1 className="text-xl font-semibold text-gray-900">Free Trial Portal</h1>
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
        {/* Trial Status Banner */}
        <div className="mb-8 bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mr-4">
                <Timer className="w-6 h-6 text-green-600" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-900">Free Trial Active</h2>
                <p className="text-gray-600">Welcome to your 1-hour AI Interview experience!</p>
              </div>
            </div>
            <div className="text-right">
              <div className={`text-3xl font-bold ${getTimeColor()}`}>
                {formatTime(timeRemaining)}
              </div>
              <p className="text-sm text-gray-500">Time Remaining</p>
            </div>
          </div>
          
          {/* Progress Bar */}
          <div className="mt-4">
            <div className="flex justify-between text-sm text-gray-600 mb-2">
              <span>Trial Progress</span>
              <span>{Math.round(progressPercentage)}% remaining</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={`h-2 rounded-full transition-all ${getProgressColor()}`}
                style={{ width: `${progressPercentage}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* Welcome Section */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Welcome, {userData?.fullName}!
          </h2>
          <p className="text-gray-600">
            Explore our AI-powered interview platform. Upload a resume, take a mock interview, and see detailed assessment reports.
          </p>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
            <div className="flex items-center mb-4">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Upload className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="ml-3 text-lg font-medium text-gray-900">Upload Resume</h3>
            </div>
            <p className="text-gray-600 mb-4">
              Upload your resume and let our AI analyze your skills and experience.
            </p>
            <button className="w-full px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors">
              Start Analysis
            </button>
          </div>

          <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
            <div className="flex items-center mb-4">
              <div className="p-2 bg-green-100 rounded-lg">
                <MessageSquare className="w-6 h-6 text-green-600" />
              </div>
              <h3 className="ml-3 text-lg font-medium text-gray-900">Mock Interview</h3>
            </div>
            <p className="text-gray-600 mb-4">
              Take a simulated interview with AI-generated questions tailored to your profile.
            </p>
            <button className="w-full px-4 py-2 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 transition-colors">
              Start Interview
            </button>
          </div>

          <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
            <div className="flex items-center mb-4">
              <div className="p-2 bg-purple-100 rounded-lg">
                <FileText className="w-6 h-6 text-purple-600" />
              </div>
              <h3 className="ml-3 text-lg font-medium text-gray-900">View Reports</h3>
            </div>
            <p className="text-gray-600 mb-4">
              Access detailed assessment reports with insights and recommendations.
            </p>
            <button className="w-full px-4 py-2 bg-purple-600 text-white font-medium rounded-lg hover:bg-purple-700 transition-colors">
              View Reports
            </button>
          </div>
        </div>

        {/* Features Overview */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">What You Can Try</h3>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="flex items-start">
                <CheckCircle className="w-5 h-5 text-green-500 mt-1 mr-3 flex-shrink-0" />
                <div>
                  <h4 className="font-medium text-gray-900">AI Resume Analysis</h4>
                  <p className="text-sm text-gray-600 mt-1">
                    Upload your resume and get instant AI-powered analysis of your skills, experience, and qualifications.
                  </p>
                </div>
              </div>
              
              <div className="flex items-start">
                <CheckCircle className="w-5 h-5 text-green-500 mt-1 mr-3 flex-shrink-0" />
                <div>
                  <h4 className="font-medium text-gray-900">Interactive Interview</h4>
                  <p className="text-sm text-gray-600 mt-1">
                    Experience our intelligent interview simulation with adaptive questions based on your background.
                  </p>
                </div>
              </div>
              
              <div className="flex items-start">
                <CheckCircle className="w-5 h-5 text-green-500 mt-1 mr-3 flex-shrink-0" />
                <div>
                  <h4 className="font-medium text-gray-900">Detailed Assessment</h4>
                  <p className="text-sm text-gray-600 mt-1">
                    Receive comprehensive reports with scoring, strengths, areas for improvement, and hiring recommendations.
                  </p>
                </div>
              </div>
              
              <div className="flex items-start">
                <CheckCircle className="w-5 h-5 text-green-500 mt-1 mr-3 flex-shrink-0" />
                <div>
                  <h4 className="font-medium text-gray-900">Real-time Feedback</h4>
                  <p className="text-sm text-gray-600 mt-1">
                    Get instant feedback on your responses and suggestions for improvement during the interview.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Upgrade Prompt */}
        <div className="mt-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-xl font-bold mb-2">Enjoying the Experience?</h3>
              <p className="text-blue-100">
                Upgrade to get unlimited access, advanced features, and detailed analytics for your hiring process.
              </p>
            </div>
            <div className="ml-6">
              <button className="bg-white text-blue-600 px-6 py-3 rounded-lg font-medium hover:bg-gray-100 transition-colors">
                Upgrade Now
              </button>
            </div>
          </div>
        </div>

        {/* Trial Expiration Warning */}
        {timeRemaining < 10 * 60 * 1000 && timeRemaining > 0 && ( // Show warning when less than 10 minutes remain and trial is not expired
          <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center">
              <AlertCircle className="w-5 h-5 text-red-500 mr-3" />
              <div>
                <h4 className="font-medium text-red-800">Trial Ending Soon</h4>
                <p className="text-sm text-red-600 mt-1">
                  Your free trial will expire in {formatTime(timeRemaining)}. Upgrade now to continue using our platform.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TrialDashboard;


