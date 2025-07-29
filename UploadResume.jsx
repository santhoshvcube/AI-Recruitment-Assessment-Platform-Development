import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  Upload, 
  FileText, 
  CheckCircle, 
  AlertCircle,
  X,
  Brain,
  Users,
  Clock,
  ArrowRight,
  Loader2
} from 'lucide-react'

const UploadResume = ({ currentUser }) => {
  const navigate = useNavigate()
  const fileInputRef = useRef(null)
  
  const [formData, setFormData] = useState({
    candidateName: '',
    candidateEmail: '',
    candidatePhone: '',
    jobTitle: '',
    jobCompany: '',
    jobDescription: ''
  })
  
  const [uploadedFile, setUploadedFile] = useState(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [processingStep, setProcessingStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [errors, setErrors] = useState({})

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }))
    }
  }

  const handleFileUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      // Validate file type
      const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
      if (!allowedTypes.includes(file.type)) {
        setErrors(prev => ({
          ...prev,
          file: 'Please upload a PDF, DOC, or DOCX file'
        }))
        return
      }
      
      // Validate file size (10MB limit)
      if (file.size > 10 * 1024 * 1024) {
        setErrors(prev => ({
          ...prev,
          file: 'File size must be less than 10MB'
        }))
        return
      }
      
      setUploadedFile(file)
      setErrors(prev => ({
        ...prev,
        file: ''
      }))
    }
  }

  const removeFile = () => {
    setUploadedFile(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const validateForm = () => {
    const newErrors = {}
    
    if (!formData.candidateName.trim()) {
      newErrors.candidateName = 'Candidate name is required'
    }
    
    if (!formData.candidateEmail.trim()) {
      newErrors.candidateEmail = 'Candidate email is required'
    } else if (!/\S+@\S+\.\S+/.test(formData.candidateEmail)) {
      newErrors.candidateEmail = 'Please enter a valid email address'
    }
    
    if (!formData.jobTitle.trim()) {
      newErrors.jobTitle = 'Job title is required'
    }
    
    if (!formData.jobCompany.trim()) {
      newErrors.jobCompany = 'Company name is required'
    }
    
    if (!formData.jobDescription.trim()) {
      newErrors.jobDescription = 'Job description is required'
    }
    
    if (!uploadedFile) {
      newErrors.file = 'Please upload a resume file'
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const simulateProcessing = async () => {
    const steps = [
      { step: 'Uploading file...', duration: 1000 },
      { step: 'Extracting text from resume...', duration: 2000 },
      { step: 'Analyzing skills and experience...', duration: 2500 },
      { step: 'Matching with job requirements...', duration: 1500 },
      { step: 'Generating interview questions...', duration: 2000 },
      { step: 'Finalizing assessment...', duration: 1000 }
    ]
    
    let currentProgress = 0
    
    for (let i = 0; i < steps.length; i++) {
      setProcessingStep(steps[i].step)
      
      // Animate progress
      const targetProgress = ((i + 1) / steps.length) * 100
      const progressIncrement = (targetProgress - currentProgress) / 20
      
      for (let j = 0; j < 20; j++) {
        currentProgress += progressIncrement
        setProgress(Math.min(currentProgress, targetProgress))
        await new Promise(resolve => setTimeout(resolve, steps[i].duration / 20))
      }
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) {
      return
    }
    
    setIsProcessing(true)
    setProgress(0)
    
    try {
      await simulateProcessing()
      
      // Mock successful processing
      setTimeout(() => {
        navigate('/dashboard')
      }, 500)
      
    } catch (error) {
      console.error('Processing error:', error)
      setErrors({ submit: 'An error occurred while processing. Please try again.' })
      setIsProcessing(false)
    }
  }

  if (!currentUser) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-blue-50">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <CardTitle>Access Denied</CardTitle>
            <CardDescription>Please log in to upload resumes.</CardDescription>
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-slate-900 mb-2">
            New Candidate Assessment
          </h1>
          <p className="text-slate-600">
            Upload a resume and job description to start the AI-powered assessment process
          </p>
        </div>

        {isProcessing ? (
          /* Processing View */
          <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
            <CardHeader className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <Brain className="h-8 w-8 text-white animate-pulse" />
              </div>
              <CardTitle>Processing Assessment</CardTitle>
              <CardDescription>
                Our AI is analyzing the resume and generating personalized interview questions
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="text-center">
                <div className="text-lg font-medium text-slate-900 mb-2">{processingStep}</div>
                <Progress value={progress} className="w-full h-3" />
                <div className="text-sm text-slate-600 mt-2">{Math.round(progress)}% complete</div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <FileText className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                  <div className="text-sm font-medium text-slate-900">Resume Analysis</div>
                  <div className="text-xs text-slate-600">Extracting key information</div>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <Brain className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                  <div className="text-sm font-medium text-slate-900">AI Processing</div>
                  <div className="text-xs text-slate-600">Matching skills & experience</div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <Users className="h-8 w-8 text-green-600 mx-auto mb-2" />
                  <div className="text-sm font-medium text-slate-900">Interview Prep</div>
                  <div className="text-xs text-slate-600">Generating questions</div>
                </div>
              </div>
            </CardContent>
          </Card>
        ) : (
          /* Upload Form */
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Candidate Information */}
            <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Users className="h-5 w-5 mr-2 text-blue-600" />
                  Candidate Information
                </CardTitle>
                <CardDescription>
                  Enter the candidate's basic information
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="candidateName">Full Name *</Label>
                    <Input
                      id="candidateName"
                      name="candidateName"
                      value={formData.candidateName}
                      onChange={handleInputChange}
                      placeholder="Enter candidate's full name"
                      className={errors.candidateName ? 'border-red-500' : ''}
                    />
                    {errors.candidateName && (
                      <p className="text-sm text-red-600 mt-1">{errors.candidateName}</p>
                    )}
                  </div>
                  
                  <div>
                    <Label htmlFor="candidateEmail">Email Address *</Label>
                    <Input
                      id="candidateEmail"
                      name="candidateEmail"
                      type="email"
                      value={formData.candidateEmail}
                      onChange={handleInputChange}
                      placeholder="candidate@email.com"
                      className={errors.candidateEmail ? 'border-red-500' : ''}
                    />
                    {errors.candidateEmail && (
                      <p className="text-sm text-red-600 mt-1">{errors.candidateEmail}</p>
                    )}
                  </div>
                </div>
                
                <div>
                  <Label htmlFor="candidatePhone">Phone Number</Label>
                  <Input
                    id="candidatePhone"
                    name="candidatePhone"
                    value={formData.candidatePhone}
                    onChange={handleInputChange}
                    placeholder="(optional)"
                  />
                </div>
              </CardContent>
            </Card>

            {/* Job Information */}
            <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <FileText className="h-5 w-5 mr-2 text-purple-600" />
                  Job Information
                </CardTitle>
                <CardDescription>
                  Provide details about the position
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="jobTitle">Job Title *</Label>
                    <Input
                      id="jobTitle"
                      name="jobTitle"
                      value={formData.jobTitle}
                      onChange={handleInputChange}
                      placeholder="e.g., Senior Software Engineer"
                      className={errors.jobTitle ? 'border-red-500' : ''}
                    />
                    {errors.jobTitle && (
                      <p className="text-sm text-red-600 mt-1">{errors.jobTitle}</p>
                    )}
                  </div>
                  
                  <div>
                    <Label htmlFor="jobCompany">Company *</Label>
                    <Input
                      id="jobCompany"
                      name="jobCompany"
                      value={formData.jobCompany}
                      onChange={handleInputChange}
                      placeholder="Company name"
                      className={errors.jobCompany ? 'border-red-500' : ''}
                    />
                    {errors.jobCompany && (
                      <p className="text-sm text-red-600 mt-1">{errors.jobCompany}</p>
                    )}
                  </div>
                </div>
                
                <div>
                  <Label htmlFor="jobDescription">Job Description *</Label>
                  <Textarea
                    id="jobDescription"
                    name="jobDescription"
                    value={formData.jobDescription}
                    onChange={handleInputChange}
                    placeholder="Paste the complete job description including requirements, responsibilities, and qualifications..."
                    rows={6}
                    className={errors.jobDescription ? 'border-red-500' : ''}
                  />
                  {errors.jobDescription && (
                    <p className="text-sm text-red-600 mt-1">{errors.jobDescription}</p>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Resume Upload */}
            <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Upload className="h-5 w-5 mr-2 text-green-600" />
                  Resume Upload
                </CardTitle>
                <CardDescription>
                  Upload the candidate's resume (PDF, DOC, or DOCX)
                </CardDescription>
              </CardHeader>
              <CardContent>
                {!uploadedFile ? (
                  <div 
                    className={`border-2 border-dashed rounded-lg p-8 text-center hover:border-blue-400 transition-colors cursor-pointer ${
                      errors.file ? 'border-red-300 bg-red-50' : 'border-slate-300 bg-slate-50'
                    }`}
                    onClick={() => fileInputRef.current?.click()}
                  >
                    <Upload className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                    <p className="text-lg font-medium text-slate-900 mb-2">
                      Click to upload resume
                    </p>
                    <p className="text-sm text-slate-600 mb-4">
                      or drag and drop your file here
                    </p>
                    <Badge variant="secondary" className="text-xs">
                      PDF, DOC, DOCX up to 10MB
                    </Badge>
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept=".pdf,.doc,.docx"
                      onChange={handleFileUpload}
                      className="hidden"
                    />
                  </div>
                ) : (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <CheckCircle className="h-5 w-5 text-green-600 mr-3" />
                        <div>
                          <p className="font-medium text-slate-900">{uploadedFile.name}</p>
                          <p className="text-sm text-slate-600">
                            {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
                          </p>
                        </div>
                      </div>
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={removeFile}
                        className="text-slate-600 hover:text-red-600"
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                )}
                
                {errors.file && (
                  <p className="text-sm text-red-600 mt-2 flex items-center">
                    <AlertCircle className="h-4 w-4 mr-1" />
                    {errors.file}
                  </p>
                )}
              </CardContent>
            </Card>

            {/* Submit */}
            <div className="flex justify-center">
              <Button 
                type="submit" 
                size="lg"
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 px-8"
                disabled={isProcessing}
              >
                {isProcessing ? (
                  <>
                    <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    Start AI Assessment
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </>
                )}
              </Button>
            </div>

            {errors.submit && (
              <div className="text-center">
                <p className="text-sm text-red-600 flex items-center justify-center">
                  <AlertCircle className="h-4 w-4 mr-1" />
                  {errors.submit}
                </p>
              </div>
            )}
          </form>
        )}
      </div>
    </div>
  )
}

export default UploadResume

