import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Eye, EyeOff, User, Shield, Mail, Phone, Lock, Clock } from 'lucide-react';

const LoginPage = () => {
  const [loginType, setLoginType] = useState('student'); // 'student', 'admin', or 'trial'
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    fullName: '', // For trial registration
    confirmPassword: '' // For trial registration
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isRegistering, setIsRegistering] = useState(false); // For trial users
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError(''); // Clear error when user types
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (loginType === 'trial' && isRegistering) {
        // Handle trial registration
        if (formData.password !== formData.confirmPassword) {
          setError('Passwords do not match');
          setLoading(false);
          return;
        }

        const response = await fetch('http://localhost:8000/api/free-trial/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: formData.email,
            full_name: formData.fullName,
            password: formData.password,
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || 'Registration failed');
        }

        const userData = {
          email: formData.email,
          fullName: formData.fullName,
          userType: 'trial',
          trialStartTime: new Date().toISOString(),
          trialEndTime: new Date(Date.now() + 60 * 60 * 1000).toISOString(), // 1 hour from now
          firstLogin: false
        };
        
        localStorage.setItem('authToken', data.access_token);
        localStorage.setItem('userData', JSON.stringify(userData));
        navigate('/trial-dashboard');

      } else if (loginType === 'trial' && !isRegistering) {
        // Handle trial login
        const response = await fetch('http://localhost:8000/api/free-trial/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
            username: formData.email,
            password: formData.password,
          }).toString(),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || 'Login failed');
        }

        const userData = {
          email: formData.email,
          userType: 'trial',
          firstLogin: false,
          trialStartTime: new Date().toISOString(), // This should come from backend
          trialEndTime: new Date(Date.now() + 60 * 60 * 1000).toISOString(), // This should come from backend
        };

        localStorage.setItem('authToken', data.access_token);
        localStorage.setItem('userData', JSON.stringify(userData));
        navigate('/trial-dashboard');

      } else {
        // Handle existing student/admin login logic
        const endpoint = loginType === 'student' ? 'http://localhost:8000/api/auth/student/login' : 'http://localhost:8000/api/auth/admin/login';
        
        const response = await fetch(endpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: formData.email,
            password: formData.password,
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || 'Login failed');
        }

        const userData = {
          email: formData.email,
          userType: loginType,
          firstLogin: loginType === 'student' && formData.password.length === 10 // Assuming mobile number is 10 digits
        };
          
        localStorage.setItem('authToken', data.access_token);
        localStorage.setItem('userData', JSON.stringify(userData));
          
        // Redirect based on user type and first login status
        if (loginType === 'student' && userData.firstLogin) {
          navigate('/change-password');
        } else if (loginType === 'student') {
          navigate('/student-dashboard');
        } else {
          navigate('/dashboard');
        }
      }
    } catch (err) {
      setError(err.message || 'An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
  };

  const renderTrialRegistrationForm = () => (
    <div className="space-y-4">
      {/* Full Name Field */}
      <div>
        <label htmlFor="fullName" className="block text-sm font-medium text-gray-700 mb-1">
          Full Name
        </label>
        <div className="relative">
          <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            id="fullName"
            name="fullName"
            value={formData.fullName}
            onChange={handleInputChange}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            placeholder="Enter your full name"
            required
          />
        </div>
      </div>

      {/* Email Field */}
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
          Email Address
        </label>
        <div className="relative">
          <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            placeholder="Enter your email"
            required
          />
        </div>
      </div>

      {/* Password Field */}
      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
          Password
        </label>
        <div className="relative">
          <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type={showPassword ? 'text' : 'password'}
            id="password"
            name="password"
            value={formData.password}
            onChange={handleInputChange}
            className="w-full pl-10 pr-12 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            placeholder="Create a password"
            required
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
          >
            {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Confirm Password Field */}
      <div>
        <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
          Confirm Password
        </label>
        <div className="relative">
          <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type={showConfirmPassword ? 'text' : 'password'}
            id="confirmPassword"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleInputChange}
            className="w-full pl-10 pr-12 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            placeholder="Confirm your password"
            required
          />
          <button
            type="button"
            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
          >
            {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
          </button>
        </div>
      </div>
    </div>
  );

  const renderLoginForm = () => (
    <div className="space-y-4">
      {/* Email Field */}
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
          Email Address
        </label>
        <div className="relative">
          <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter your email"
            required
          />
        </div>
      </div>

      {/* Password Field */}
      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
          {loginType === 'student' ? 'Password (Mobile Number for first login)' : 'Password'}
        </label>
        <div className="relative">
          {loginType === 'student' ? (
            <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          ) : (
            <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          )}
          <input
            type={showPassword ? 'text' : 'password'}
            id="password"
            name="password"
            value={formData.password}
            onChange={handleInputChange}
            className="w-full pl-10 pr-12 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder={loginType === 'student' ? 'Enter mobile number or password' : 'Enter your password'}
            required
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
          >
            {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
          </button>
        </div>
        {loginType === 'student' && (
          <p className="text-xs text-gray-500 mt-1">
            First-time login: Use your mobile number as password
          </p>
        )}
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
              <span className="text-white font-bold text-xl">AI</span>
            </div>
          </div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Welcome Back</h1>
          <p className="text-gray-600">Sign in to your account</p>
        </div>

        {/* Login Type Selector */}
        <div className="bg-gray-100 rounded-lg p-1 mb-6">
          <div className="grid grid-cols-3 gap-1">
            <button
              type="button"
              onClick={() => {
                setLoginType('student');
                setIsRegistering(false);
              }}
              className={`flex items-center justify-center py-2 px-2 rounded-md text-xs font-medium transition-all ${
                loginType === 'student'
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <User className="w-3 h-3 mr-1" />
              VCube Student
            </button>
            <button
              type="button"
              onClick={() => {
                setLoginType('admin');
                setIsRegistering(false);
              }}
              className={`flex items-center justify-center py-2 px-2 rounded-md text-xs font-medium transition-all ${
                loginType === 'admin'
                  ? 'bg-white text-purple-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <Shield className="w-3 h-3 mr-1" />
              Admin
            </button>
            <button
              type="button"
              onClick={() => {
                setLoginType('trial');
                setIsRegistering(true);
              }}
              className={`flex items-center justify-center py-2 px-2 rounded-md text-xs font-medium transition-all ${
                loginType === 'trial'
                  ? 'bg-white text-green-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <Clock className="w-3 h-3 mr-1" />
              Free Trial
            </button>
          </div>
        </div>

        {/* Login Form */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          {loginType === 'trial' && (
            <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-center text-green-700">
                <Clock className="w-4 h-4 mr-2" />
                <span className="text-sm font-medium">
                  {isRegistering ? 'Get 1 Hour Free Trial' : 'Trial Login'}
                </span>
              </div>
              <p className="text-xs text-green-600 mt-1">
                {isRegistering 
                  ? 'Register now and get instant access to our AI interview platform for 1 hour.'
                  : 'Sign in to continue your free trial session.'
                }
              </p>
            </div>
          )}

          <form onSubmit={handleSubmit}>
            {loginType === 'trial' && isRegistering ? renderTrialRegistrationForm() : renderLoginForm()}

            {/* Error Message */}
            {error && (
              <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-3">
                <p className="text-red-600 text-sm">{error}</p>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className={`w-full mt-6 py-2 px-4 rounded-lg font-medium transition-all ${
                loginType === 'student'
                  ? 'bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800'
                  : loginType === 'admin'
                  ? 'bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800'
                  : 'bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800'
              } text-white ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                  {loginType === 'trial' && isRegistering ? 'Creating Account...' : 'Signing in...'}
                </div>
              ) : (
                loginType === 'trial' && isRegistering 
                  ? 'Start Free Trial' 
                  : `Sign in as ${loginType === 'student' ? 'VCube Student' : loginType === 'admin' ? 'Admin' : 'Trial User'}`
              )}
            </button>
          </form>

          {/* Additional Links */}
          <div className="mt-6 text-center">
            {loginType === 'trial' ? (
              <div className="space-y-2">
                <button
                  type="button"
                  onClick={() => setIsRegistering(!isRegistering)}
                  className="text-green-600 hover:text-green-700 text-sm font-medium"
                >
                  {isRegistering ? 'Already have a trial account? Sign in' : 'New user? Start free trial'}
                </button>
                <p className="text-xs text-gray-500">
                  No credit card required. Instant access for 1 hour.
                </p>
              </div>
            ) : loginType === 'student' ? (
              <div className="space-y-2">
                <p className="text-sm text-gray-600">
                  First time here? Contact your administrator for registration.
                </p>
                <button
                  type="button"
                  className="text-blue-600 hover:text-blue-700 text-sm font-medium"
                >
                  Forgot Password?
                </button>
              </div>
            ) : (
              <div className="space-y-2">
                <button
                  type="button"
                  className="text-purple-600 hover:text-purple-700 text-sm font-medium"
                >
                  Forgot Password?
                </button>
                <p className="text-xs text-gray-500">
                  Admin access is restricted. Contact system administrator for support.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-6">
          <p className="text-xs text-gray-500">
            By signing in, you agree to our Terms of Service and Privacy Policy
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;

