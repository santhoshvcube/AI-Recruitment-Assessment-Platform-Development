import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { 
  Users, 
  FileText, 
  BarChart3, 
  Clock,
  TrendingUp,
  CheckCircle,
  AlertCircle,
  Plus,
  Eye,
  Download,
  Calendar,
  Star
} from 'lucide-react'

const Dashboard = ({ currentUser }) => {
  const [stats, setStats] = useState({
    totalCandidates: 0,
    completedAssessments: 0,
    pendingReviews: 0,
    averageScore: 0
  })

  const [recentAssessments, setRecentAssessments] = useState([])

  useEffect(() => {
    // Mock data - in real app, fetch from API
    setStats({
      totalCandidates: 47,
      completedAssessments: 32,
      pendingReviews: 8,
      averageScore: 78.5
    })

    setRecentAssessments([
      {
        id: 1,
        candidateName: "Sarah Johnson",
        position: "Senior Frontend Developer",
        score: 92,
        status: "completed",
        date: "2024-01-20",
        recommendation: "strong_hire"
      },
      {
        id: 2,
        candidateName: "Michael Chen",
        position: "Data Scientist",
        score: 85,
        status: "completed",
        date: "2024-01-19",
        recommendation: "hire"
      },
      {
        id: 3,
        candidateName: "Emily Rodriguez",
        position: "UX Designer",
        score: 88,
        status: "in_progress",
        date: "2024-01-18",
        recommendation: null
      },
      {
        id: 4,
        candidateName: "David Kim",
        position: "Backend Engineer",
        score: 76,
        status: "completed",
        date: "2024-01-17",
        recommendation: "maybe"
      },
      {
        id: 5,
        candidateName: "Lisa Wang",
        position: "Product Manager",
        score: 94,
        status: "completed",
        date: "2024-01-16",
        recommendation: "strong_hire"
      }
    ])
  }, [])

  const getStatusBadge = (status) => {
    switch (status) {
      case 'completed':
        return <Badge className="bg-green-100 text-green-700">Completed</Badge>
      case 'in_progress':
        return <Badge className="bg-blue-100 text-blue-700">In Progress</Badge>
      case 'pending':
        return <Badge className="bg-yellow-100 text-yellow-700">Pending</Badge>
      default:
        return <Badge variant="secondary">Unknown</Badge>
    }
  }

  const getRecommendationBadge = (recommendation) => {
    switch (recommendation) {
      case 'strong_hire':
        return <Badge className="bg-green-100 text-green-700">Strong Hire</Badge>
      case 'hire':
        return <Badge className="bg-blue-100 text-blue-700">Hire</Badge>
      case 'maybe':
        return <Badge className="bg-yellow-100 text-yellow-700">Maybe</Badge>
      case 'no_hire':
        return <Badge className="bg-red-100 text-red-700">No Hire</Badge>
      default:
        return null
    }
  }

  const getScoreColor = (score) => {
    if (score >= 85) return 'text-green-600'
    if (score >= 70) return 'text-blue-600'
    if (score >= 55) return 'text-yellow-600'
    return 'text-red-600'
  }

  if (!currentUser) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <CardTitle>Access Denied</CardTitle>
            <CardDescription>Please log in to access the dashboard.</CardDescription>
          </CardHeader>
          <CardContent>
            <Link to="/">
              <Button className="w-full">Go to Home</Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900 mb-2">
            Welcome back, {currentUser.name}
          </h1>
          <p className="text-slate-600">
            Here's an overview of your recruitment activities and candidate assessments.
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-white/60 backdrop-blur-sm border-slate-200 hover:shadow-lg transition-all duration-300">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-600">Total Candidates</CardTitle>
              <Users className="h-4 w-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-slate-900">{stats.totalCandidates}</div>
              <p className="text-xs text-slate-600 mt-1">
                <TrendingUp className="inline h-3 w-3 mr-1" />
                +12% from last month
              </p>
            </CardContent>
          </Card>

          <Card className="bg-white/60 backdrop-blur-sm border-slate-200 hover:shadow-lg transition-all duration-300">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-600">Completed Assessments</CardTitle>
              <CheckCircle className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-slate-900">{stats.completedAssessments}</div>
              <p className="text-xs text-slate-600 mt-1">
                <Clock className="inline h-3 w-3 mr-1" />
                {stats.pendingReviews} pending review
              </p>
            </CardContent>
          </Card>

          <Card className="bg-white/60 backdrop-blur-sm border-slate-200 hover:shadow-lg transition-all duration-300">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-600">Average Score</CardTitle>
              <BarChart3 className="h-4 w-4 text-purple-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-slate-900">{stats.averageScore}%</div>
              <Progress value={stats.averageScore} className="mt-2" />
            </CardContent>
          </Card>

          <Card className="bg-white/60 backdrop-blur-sm border-slate-200 hover:shadow-lg transition-all duration-300">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-600">This Month</CardTitle>
              <Calendar className="h-4 w-4 text-orange-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-slate-900">15</div>
              <p className="text-xs text-slate-600 mt-1">
                <Star className="inline h-3 w-3 mr-1" />
                New assessments
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <Card className="lg:col-span-2 bg-white/60 backdrop-blur-sm border-slate-200">
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                Recent Assessments
                <Link to="/reports">
                  <Button variant="outline" size="sm">
                    View All
                    <Eye className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              </CardTitle>
              <CardDescription>
                Latest candidate assessments and their results
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentAssessments.map((assessment) => (
                  <div key={assessment.id} className="flex items-center justify-between p-4 bg-white rounded-lg border border-slate-200 hover:shadow-md transition-all duration-200">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h4 className="font-medium text-slate-900">{assessment.candidateName}</h4>
                        {getStatusBadge(assessment.status)}
                        {assessment.recommendation && getRecommendationBadge(assessment.recommendation)}
                      </div>
                      <p className="text-sm text-slate-600 mb-1">{assessment.position}</p>
                      <p className="text-xs text-slate-500">{assessment.date}</p>
                    </div>
                    <div className="text-right">
                      <div className={`text-2xl font-bold ${getScoreColor(assessment.score)}`}>
                        {assessment.score}%
                      </div>
                      <div className="flex space-x-2 mt-2">
                        <Button variant="outline" size="sm">
                          <Eye className="h-3 w-3" />
                        </Button>
                        <Button variant="outline" size="sm">
                          <Download className="h-3 w-3" />
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
              <CardDescription>
                Start a new assessment or manage existing ones
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Link to="/upload">
                <Button className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                  <Plus className="mr-2 h-4 w-4" />
                  New Assessment
                </Button>
              </Link>
              
              <Link to="/reports">
                <Button variant="outline" className="w-full">
                  <FileText className="mr-2 h-4 w-4" />
                  View Reports
                </Button>
              </Link>
              
              <Button variant="outline" className="w-full">
                <BarChart3 className="mr-2 h-4 w-4" />
                Analytics
              </Button>
              
              <Button variant="outline" className="w-full">
                <Users className="mr-2 h-4 w-4" />
                Manage Candidates
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Performance Overview */}
        <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
          <CardHeader>
            <CardTitle>Performance Overview</CardTitle>
            <CardDescription>
              Assessment trends and hiring insights
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center p-6 bg-gradient-to-r from-blue-50 to-cyan-50 rounded-lg">
                <div className="text-3xl font-bold text-blue-600 mb-2">85%</div>
                <div className="text-sm text-slate-600">Interview Completion Rate</div>
              </div>
              <div className="text-center p-6 bg-gradient-to-r from-green-50 to-teal-50 rounded-lg">
                <div className="text-3xl font-bold text-green-600 mb-2">92%</div>
                <div className="text-sm text-slate-600">Assessment Accuracy</div>
              </div>
              <div className="text-center p-6 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg">
                <div className="text-3xl font-bold text-purple-600 mb-2">4.8</div>
                <div className="text-sm text-slate-600">Average Rating</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default Dashboard

