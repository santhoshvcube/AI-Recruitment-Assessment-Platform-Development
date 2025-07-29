import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  MessageSquare, 
  Clock, 
  CheckCircle, 
  ArrowRight,
  ArrowLeft,
  Pause,
  Play,
  RotateCcw,
  Brain,
  Star,
  AlertCircle,
  Timer
} from 'lucide-react'

const Interview = ({ currentUser }) => {
  const { sessionId } = useParams()
  const navigate = useNavigate()
  
  const [interviewState, setInterviewState] = useState({
    currentQuestionIndex: 0,
    totalQuestions: 10,
    isActive: true,
    isPaused: false,
    timeRemaining: 1800, // 30 minutes
    startTime: Date.now()
  })
  
  const [currentQuestion, setCurrentQuestion] = useState(null)
  const [currentAnswer, setCurrentAnswer] = useState('')
  const [responses, setResponses] = useState([])
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [showResults, setShowResults] = useState(false)

  // Mock interview questions
  const mockQuestions = [
    {
      id: 1,
      question: "Tell me about your experience with React and how you've used it in previous projects.",
      category: "Technical",
      type: "experience",
      difficulty: "medium",
      estimatedTime: 3
    },
    {
      id: 2,
      question: "Describe a challenging problem you solved in your last role and walk me through your approach.",
      category: "Problem Solving",
      type: "behavioral",
      difficulty: "medium",
      estimatedTime: 4
    },
    {
      id: 3,
      question: "How do you handle working with tight deadlines and multiple priorities?",
      category: "Work Style",
      type: "behavioral",
      difficulty: "easy",
      estimatedTime: 3
    },
    {
      id: 4,
      question: "Explain the concept of state management in React applications. What are some popular solutions?",
      category: "Technical",
      type: "knowledge",
      difficulty: "medium",
      estimatedTime: 4
    },
    {
      id: 5,
      question: "Tell me about a time when you had to learn a new technology quickly. How did you approach it?",
      category: "Learning",
      type: "behavioral",
      difficulty: "easy",
      estimatedTime: 3
    }
  ]

  useEffect(() => {
    // Initialize interview session
    if (mockQuestions.length > 0) {
      setCurrentQuestion(mockQuestions[0])
    }

    // Timer countdown
    const timer = setInterval(() => {
      if (interviewState.isActive && !interviewState.isPaused) {
        setInterviewState(prev => ({
          ...prev,
          timeRemaining: Math.max(0, prev.timeRemaining - 1)
        }))
      }
    }, 1000)

    return () => clearInterval(timer)
  }, [interviewState.isActive, interviewState.isPaused])

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = seconds % 60
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
  }

  const getCategoryColor = (category) => {
    switch (category) {
      case 'Technical':
        return 'bg-blue-100 text-blue-700'
      case 'Problem Solving':
        return 'bg-purple-100 text-purple-700'
      case 'Work Style':
        return 'bg-green-100 text-green-700'
      case 'Learning':
        return 'bg-orange-100 text-orange-700'
      default:
        return 'bg-gray-100 text-gray-700'
    }
  }

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'easy':
        return 'bg-green-100 text-green-700'
      case 'medium':
        return 'bg-yellow-100 text-yellow-700'
      case 'hard':
        return 'bg-red-100 text-red-700'
      default:
        return 'bg-gray-100 text-gray-700'
    }
  }

  const handleSubmitAnswer = async () => {
    if (!currentAnswer.trim()) {
      return
    }

    setIsSubmitting(true)

    // Mock API call delay
    await new Promise(resolve => setTimeout(resolve, 1000))

    // Save response
    const response = {
      questionId: currentQuestion.id,
      question: currentQuestion.question,
      answer: currentAnswer,
      timestamp: Date.now(),
      timeSpent: Math.floor((Date.now() - interviewState.startTime) / 1000)
    }

    setResponses(prev => [...prev, response])
    setCurrentAnswer('')

    // Move to next question or finish
    const nextIndex = interviewState.currentQuestionIndex + 1
    if (nextIndex < mockQuestions.length) {
      setCurrentQuestion(mockQuestions[nextIndex])
      setInterviewState(prev => ({
        ...prev,
        currentQuestionIndex: nextIndex
      }))
    } else {
      // Interview completed
      setShowResults(true)
      setInterviewState(prev => ({
        ...prev,
        isActive: false
      }))
    }

    setIsSubmitting(false)
  }

  const handlePauseResume = () => {
    setInterviewState(prev => ({
      ...prev,
      isPaused: !prev.isPaused
    }))
  }

  const handlePreviousQuestion = () => {
    if (interviewState.currentQuestionIndex > 0) {
      const prevIndex = interviewState.currentQuestionIndex - 1
      setCurrentQuestion(mockQuestions[prevIndex])
      setInterviewState(prev => ({
        ...prev,
        currentQuestionIndex: prevIndex
      }))
      
      // Load previous answer if exists
      const prevResponse = responses.find(r => r.questionId === mockQuestions[prevIndex].id)
      if (prevResponse) {
        setCurrentAnswer(prevResponse.answer)
      }
    }
  }

  const handleFinishInterview = () => {
    navigate('/reports')
  }

  if (!currentUser) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-blue-50">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <CardTitle>Access Denied</CardTitle>
            <CardDescription>Please log in to access the interview.</CardDescription>
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

  if (showResults) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
            <CardHeader className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-green-500 to-teal-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="h-8 w-8 text-white" />
              </div>
              <CardTitle className="text-2xl">Interview Completed!</CardTitle>
              <CardDescription>
                Thank you for completing the AI interview assessment
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">{responses.length}</div>
                  <div className="text-sm text-slate-600">Questions Answered</div>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600">
                    {formatTime(Math.floor((Date.now() - interviewState.startTime) / 1000))}
                  </div>
                  <div className="text-sm text-slate-600">Total Time</div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">95%</div>
                  <div className="text-sm text-slate-600">Completion Rate</div>
                </div>
              </div>

              <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-slate-900 mb-3">What's Next?</h3>
                <ul className="space-y-2 text-slate-700">
                  <li className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                    Your responses are being analyzed by our AI system
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                    A comprehensive assessment report will be generated
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                    Results will be available in the reports section
                  </li>
                </ul>
              </div>

              <div className="flex justify-center space-x-4">
                <Button 
                  onClick={handleFinishInterview}
                  className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                >
                  View Assessment Report
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
                <Button variant="outline" onClick={() => navigate('/dashboard')}>
                  Back to Dashboard
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-2xl font-bold text-slate-900">AI Interview Session</h1>
            <div className="flex items-center space-x-4">
              <Badge className={`${interviewState.isPaused ? 'bg-yellow-100 text-yellow-700' : 'bg-green-100 text-green-700'}`}>
                {interviewState.isPaused ? 'Paused' : 'Active'}
              </Badge>
              <div className="flex items-center text-slate-600">
                <Timer className="h-4 w-4 mr-1" />
                {formatTime(interviewState.timeRemaining)}
              </div>
            </div>
          </div>
          
          {/* Progress */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm text-slate-600">
              <span>Question {interviewState.currentQuestionIndex + 1} of {mockQuestions.length}</span>
              <span>{Math.round(((interviewState.currentQuestionIndex + 1) / mockQuestions.length) * 100)}% Complete</span>
            </div>
            <Progress value={((interviewState.currentQuestionIndex + 1) / mockQuestions.length) * 100} className="h-2" />
          </div>
        </div>

        {/* Question Card */}
        {currentQuestion && (
          <Card className="bg-white/60 backdrop-blur-sm border-slate-200 mb-6">
            <CardHeader>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-2">
                  <Badge className={getCategoryColor(currentQuestion.category)}>
                    {currentQuestion.category}
                  </Badge>
                  <Badge className={getDifficultyColor(currentQuestion.difficulty)}>
                    {currentQuestion.difficulty}
                  </Badge>
                </div>
                <div className="flex items-center text-sm text-slate-600">
                  <Clock className="h-4 w-4 mr-1" />
                  ~{currentQuestion.estimatedTime} min
                </div>
              </div>
              <CardTitle className="text-xl leading-relaxed">
                {currentQuestion.question}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <Textarea
                  value={currentAnswer}
                  onChange={(e) => setCurrentAnswer(e.target.value)}
                  placeholder="Type your answer here..."
                  rows={8}
                  className="resize-none"
                  disabled={interviewState.isPaused}
                />
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={handlePauseResume}
                      className="flex items-center"
                    >
                      {interviewState.isPaused ? (
                        <>
                          <Play className="h-4 w-4 mr-1" />
                          Resume
                        </>
                      ) : (
                        <>
                          <Pause className="h-4 w-4 mr-1" />
                          Pause
                        </>
                      )}
                    </Button>
                    
                    {interviewState.currentQuestionIndex > 0 && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={handlePreviousQuestion}
                        disabled={isSubmitting}
                      >
                        <ArrowLeft className="h-4 w-4 mr-1" />
                        Previous
                      </Button>
                    )}
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <div className="text-sm text-slate-600">
                      {currentAnswer.length} characters
                    </div>
                    <Button
                      onClick={handleSubmitAnswer}
                      disabled={!currentAnswer.trim() || isSubmitting || interviewState.isPaused}
                      className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                    >
                      {isSubmitting ? (
                        <>
                          <Brain className="h-4 w-4 mr-2 animate-pulse" />
                          Analyzing...
                        </>
                      ) : interviewState.currentQuestionIndex === mockQuestions.length - 1 ? (
                        <>
                          Finish Interview
                          <CheckCircle className="h-4 w-4 ml-2" />
                        </>
                      ) : (
                        <>
                          Next Question
                          <ArrowRight className="h-4 w-4 ml-2" />
                        </>
                      )}
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Tips Card */}
        <Card className="bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
          <CardContent className="p-4">
            <div className="flex items-start space-x-3">
              <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                <Star className="h-4 w-4 text-blue-600" />
              </div>
              <div>
                <h4 className="font-medium text-slate-900 mb-1">Interview Tips</h4>
                <ul className="text-sm text-slate-700 space-y-1">
                  <li>• Be specific and provide concrete examples</li>
                  <li>• Take your time to think before answering</li>
                  <li>• Use the STAR method (Situation, Task, Action, Result) for behavioral questions</li>
                  <li>• You can pause the interview if you need a break</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Warning for low time */}
        {interviewState.timeRemaining < 300 && interviewState.timeRemaining > 0 && (
          <Card className="mt-4 bg-yellow-50 border-yellow-200">
            <CardContent className="p-4">
              <div className="flex items-center space-x-2 text-yellow-800">
                <AlertCircle className="h-5 w-5" />
                <span className="font-medium">
                  Warning: Only {formatTime(interviewState.timeRemaining)} remaining
                </span>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

export default Interview

