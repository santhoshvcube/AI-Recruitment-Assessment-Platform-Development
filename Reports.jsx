import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Input } from '@/components/ui/input.jsx'
import { 
  FileText, 
  Download, 
  Eye, 
  Search,
  Filter,
  Calendar,
  BarChart3,
  TrendingUp,
  Users,
  CheckCircle,
  AlertCircle,
  Star,
  Clock,
  ArrowUpRight
} from 'lucide-react'

const Reports = ({ currentUser }) => {
  const navigate = useNavigate()
  const [reports, setReports] = useState([])
  const [filteredReports, setFilteredReports] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedFilter, setSelectedFilter] = useState('all')
  const [selectedReport, setSelectedReport] = useState(null)

  useEffect(() => {
    // Mock reports data
    const mockReports = [
      {
        id: 1,
        candidateName: "Sarah Johnson",
        position: "Senior Frontend Developer",
        company: "TechCorp",
        overallScore: 92,
        confidenceLevel: 88,
        recommendation: "strong_hire",
        status: "completed",
        date: "2024-01-20",
        componentScores: {
          resumeAnalysis: 95,
          skillMatch: 90,
          experienceRelevance: 88,
          interviewPerformance: 94,
          culturalFit: 85
        },
        strengths: [
          "Excellent React and TypeScript expertise",
          "Strong problem-solving abilities",
          "Great communication skills",
          "Leadership experience"
        ],
        developmentAreas: [
          "Could benefit from more backend experience",
          "Limited experience with cloud platforms"
        ],
        riskFactors: [],
        interviewDuration: "45 minutes"
      },
      {
        id: 2,
        candidateName: "Michael Chen",
        position: "Data Scientist",
        company: "DataLab",
        overallScore: 85,
        confidenceLevel: 82,
        recommendation: "hire",
        status: "completed",
        date: "2024-01-19",
        componentScores: {
          resumeAnalysis: 88,
          skillMatch: 85,
          experienceRelevance: 90,
          interviewPerformance: 80,
          culturalFit: 82
        },
        strengths: [
          "Strong statistical analysis skills",
          "Proficient in Python and R",
          "Machine learning expertise",
          "Research background"
        ],
        developmentAreas: [
          "Communication could be clearer",
          "Limited business domain knowledge"
        ],
        riskFactors: [
          {
            type: "communication",
            description: "May need support in presenting to non-technical stakeholders"
          }
        ],
        interviewDuration: "50 minutes"
      },
      {
        id: 3,
        candidateName: "Emily Rodriguez",
        position: "UX Designer",
        company: "DesignStudio",
        overallScore: 88,
        confidenceLevel: 85,
        recommendation: "hire",
        status: "in_progress",
        date: "2024-01-18",
        componentScores: {
          resumeAnalysis: 90,
          skillMatch: 88,
          experienceRelevance: 85,
          interviewPerformance: null,
          culturalFit: null
        },
        strengths: [
          "Excellent design portfolio",
          "User research experience",
          "Figma and Adobe expertise"
        ],
        developmentAreas: [],
        riskFactors: [],
        interviewDuration: null
      },
      {
        id: 4,
        candidateName: "David Kim",
        position: "Backend Engineer",
        company: "CloudTech",
        overallScore: 76,
        confidenceLevel: 78,
        recommendation: "maybe",
        status: "completed",
        date: "2024-01-17",
        componentScores: {
          resumeAnalysis: 80,
          skillMatch: 75,
          experienceRelevance: 70,
          interviewPerformance: 78,
          culturalFit: 75
        },
        strengths: [
          "Solid Java and Spring experience",
          "Database design skills",
          "System architecture knowledge"
        ],
        developmentAreas: [
          "Limited cloud platform experience",
          "Needs improvement in testing practices",
          "Communication skills need development"
        ],
        riskFactors: [
          {
            type: "experience_gap",
            description: "May require additional training in modern DevOps practices"
          }
        ],
        interviewDuration: "40 minutes"
      },
      {
        id: 5,
        candidateName: "Lisa Wang",
        position: "Product Manager",
        company: "InnovateLab",
        overallScore: 94,
        confidenceLevel: 91,
        recommendation: "strong_hire",
        status: "completed",
        date: "2024-01-16",
        componentScores: {
          resumeAnalysis: 95,
          skillMatch: 92,
          experienceRelevance: 96,
          interviewPerformance: 95,
          culturalFit: 92
        },
        strengths: [
          "Exceptional product strategy skills",
          "Strong analytical thinking",
          "Excellent stakeholder management",
          "Data-driven decision making",
          "Leadership and team building"
        ],
        developmentAreas: [
          "Could benefit from more technical depth"
        ],
        riskFactors: [],
        interviewDuration: "55 minutes"
      }
    ]

    setReports(mockReports)
    setFilteredReports(mockReports)
  }, [])

  useEffect(() => {
    let filtered = reports

    // Apply search filter
    if (searchTerm) {
      filtered = filtered.filter(report => 
        report.candidateName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        report.position.toLowerCase().includes(searchTerm.toLowerCase()) ||
        report.company.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    // Apply status filter
    if (selectedFilter !== 'all') {
      if (selectedFilter === 'strong_hire') {
        filtered = filtered.filter(report => report.recommendation === 'strong_hire')
      } else if (selectedFilter === 'hire') {
        filtered = filtered.filter(report => report.recommendation === 'hire')
      } else if (selectedFilter === 'maybe') {
        filtered = filtered.filter(report => report.recommendation === 'maybe')
      } else if (selectedFilter === 'completed') {
        filtered = filtered.filter(report => report.status === 'completed')
      } else if (selectedFilter === 'in_progress') {
        filtered = filtered.filter(report => report.status === 'in_progress')
      }
    }

    setFilteredReports(filtered)
  }, [searchTerm, selectedFilter, reports])

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
        return <Badge variant="secondary">Pending</Badge>
    }
  }

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

  const getScoreColor = (score) => {
    if (score >= 85) return 'text-green-600'
    if (score >= 70) return 'text-blue-600'
    if (score >= 55) return 'text-yellow-600'
    return 'text-red-600'
  }

  const handleViewReport = (report) => {
    setSelectedReport(report)
  }

  const handleDownloadReport = (reportId) => {
    // Mock download functionality
    console.log(`Downloading report ${reportId}`)
  }

  if (!currentUser) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-blue-50">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <CardTitle>Access Denied</CardTitle>
            <CardDescription>Please log in to view reports.</CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => navigate('/')} className="w-full">
              Go to Home
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (selectedReport) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 py-8">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div>
              <Button 
                variant="outline" 
                onClick={() => setSelectedReport(null)}
                className="mb-2"
              >
                ← Back to Reports
              </Button>
              <h1 className="text-3xl font-bold text-slate-900">
                Assessment Report: {selectedReport.candidateName}
              </h1>
              <p className="text-slate-600">
                {selectedReport.position} at {selectedReport.company}
              </p>
            </div>
            <div className="flex space-x-2">
              <Button variant="outline" onClick={() => handleDownloadReport(selectedReport.id)}>
                <Download className="h-4 w-4 mr-2" />
                Download PDF
              </Button>
            </div>
          </div>

          {/* Overall Assessment */}
          <Card className="bg-white/60 backdrop-blur-sm border-slate-200 mb-6">
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                Overall Assessment
                {getRecommendationBadge(selectedReport.recommendation)}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className={`text-4xl font-bold ${getScoreColor(selectedReport.overallScore)} mb-2`}>
                    {selectedReport.overallScore}%
                  </div>
                  <div className="text-slate-600">Overall Score</div>
                </div>
                <div className="text-center">
                  <div className={`text-4xl font-bold ${getScoreColor(selectedReport.confidenceLevel)} mb-2`}>
                    {selectedReport.confidenceLevel}%
                  </div>
                  <div className="text-slate-600">Confidence Level</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-slate-900 mb-2">
                    {selectedReport.interviewDuration || 'N/A'}
                  </div>
                  <div className="text-slate-600">Interview Duration</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Component Scores */}
          <Card className="bg-white/60 backdrop-blur-sm border-slate-200 mb-6">
            <CardHeader>
              <CardTitle>Detailed Scores</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Object.entries(selectedReport.componentScores).map(([component, score]) => (
                  <div key={component}>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-slate-700 capitalize">
                        {component.replace(/([A-Z])/g, ' $1').trim()}
                      </span>
                      <span className={`font-semibold ${score ? getScoreColor(score) : 'text-slate-400'}`}>
                        {score ? `${score}%` : 'Pending'}
                      </span>
                    </div>
                    <Progress value={score || 0} className="h-2" />
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Strengths */}
            <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
              <CardHeader>
                <CardTitle className="flex items-center text-green-700">
                  <CheckCircle className="h-5 w-5 mr-2" />
                  Key Strengths
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3">
                  {selectedReport.strengths.map((strength, index) => (
                    <li key={index} className="flex items-start">
                      <Star className="h-4 w-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-slate-700">{strength}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            {/* Development Areas */}
            <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
              <CardHeader>
                <CardTitle className="flex items-center text-blue-700">
                  <TrendingUp className="h-5 w-5 mr-2" />
                  Development Areas
                </CardTitle>
              </CardHeader>
              <CardContent>
                {selectedReport.developmentAreas.length > 0 ? (
                  <ul className="space-y-3">
                    {selectedReport.developmentAreas.map((area, index) => (
                      <li key={index} className="flex items-start">
                        <ArrowUpRight className="h-4 w-4 text-blue-500 mr-2 mt-0.5 flex-shrink-0" />
                        <span className="text-slate-700">{area}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-slate-600 italic">No significant development areas identified.</p>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Risk Factors */}
          {selectedReport.riskFactors.length > 0 && (
            <Card className="bg-white/60 backdrop-blur-sm border-slate-200 mt-6">
              <CardHeader>
                <CardTitle className="flex items-center text-orange-700">
                  <AlertCircle className="h-5 w-5 mr-2" />
                  Risk Factors
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {selectedReport.riskFactors.map((risk, index) => (
                    <div key={index} className="bg-orange-50 border border-orange-200 rounded-lg p-4">
                      <div className="font-medium text-orange-800 capitalize mb-1">
                        {risk.type.replace('_', ' ')}
                      </div>
                      <div className="text-orange-700">{risk.description}</div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900 mb-2">Assessment Reports</h1>
          <p className="text-slate-600">
            View and manage candidate assessment reports and hiring recommendations.
          </p>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-slate-900">{reports.length}</div>
                  <div className="text-sm text-slate-600">Total Reports</div>
                </div>
                <FileText className="h-8 w-8 text-blue-600" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-green-600">
                    {reports.filter(r => r.recommendation === 'strong_hire').length}
                  </div>
                  <div className="text-sm text-slate-600">Strong Hires</div>
                </div>
                <CheckCircle className="h-8 w-8 text-green-600" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-slate-900">
                    {Math.round(reports.reduce((acc, r) => acc + r.overallScore, 0) / reports.length)}%
                  </div>
                  <div className="text-sm text-slate-600">Avg Score</div>
                </div>
                <BarChart3 className="h-8 w-8 text-purple-600" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-slate-900">
                    {reports.filter(r => r.status === 'in_progress').length}
                  </div>
                  <div className="text-sm text-slate-600">In Progress</div>
                </div>
                <Clock className="h-8 w-8 text-orange-600" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Filters */}
        <Card className="bg-white/60 backdrop-blur-sm border-slate-200 mb-6">
          <CardContent className="p-4">
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
                  <Input
                    placeholder="Search candidates, positions, or companies..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>
              <div className="flex gap-2">
                <Button
                  variant={selectedFilter === 'all' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setSelectedFilter('all')}
                >
                  All
                </Button>
                <Button
                  variant={selectedFilter === 'strong_hire' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setSelectedFilter('strong_hire')}
                >
                  Strong Hire
                </Button>
                <Button
                  variant={selectedFilter === 'hire' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setSelectedFilter('hire')}
                >
                  Hire
                </Button>
                <Button
                  variant={selectedFilter === 'maybe' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setSelectedFilter('maybe')}
                >
                  Maybe
                </Button>
                <Button
                  variant={selectedFilter === 'completed' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setSelectedFilter('completed')}
                >
                  Completed
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Reports List */}
        <div className="space-y-4">
          {filteredReports.map((report) => (
            <Card key={report.id} className="bg-white/60 backdrop-blur-sm border-slate-200 hover:shadow-lg transition-all duration-200">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className="text-lg font-semibold text-slate-900">{report.candidateName}</h3>
                      {getStatusBadge(report.status)}
                      {report.recommendation && getRecommendationBadge(report.recommendation)}
                    </div>
                    <p className="text-slate-600 mb-1">{report.position} at {report.company}</p>
                    <div className="flex items-center space-x-4 text-sm text-slate-500">
                      <span className="flex items-center">
                        <Calendar className="h-4 w-4 mr-1" />
                        {report.date}
                      </span>
                      {report.interviewDuration && (
                        <span className="flex items-center">
                          <Clock className="h-4 w-4 mr-1" />
                          {report.interviewDuration}
                        </span>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-6">
                    <div className="text-center">
                      <div className={`text-2xl font-bold ${getScoreColor(report.overallScore)}`}>
                        {report.overallScore}%
                      </div>
                      <div className="text-xs text-slate-600">Overall Score</div>
                    </div>
                    
                    <div className="flex space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleViewReport(report)}
                      >
                        <Eye className="h-4 w-4 mr-1" />
                        View
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleDownloadReport(report.id)}
                      >
                        <Download className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {filteredReports.length === 0 && (
          <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
            <CardContent className="p-12 text-center">
              <FileText className="h-12 w-12 text-slate-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-slate-900 mb-2">No reports found</h3>
              <p className="text-slate-600 mb-4">
                {searchTerm || selectedFilter !== 'all' 
                  ? 'Try adjusting your search or filter criteria.'
                  : 'Start by uploading a resume to generate your first assessment report.'
                }
              </p>
              {!searchTerm && selectedFilter === 'all' && (
                <Button onClick={() => navigate('/upload')}>
                  Upload Resume
                </Button>
              )}
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

export default Reports

