import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Button } from '@/components/ui/button.jsx'
import { 
  Upload, 
  Brain, 
  MessageSquare, 
  FileText,
  ArrowRight,
  CheckCircle,
  Clock,
  Users,
  BarChart3
} from 'lucide-react'

const HowItWorks = () => {
  const steps = [
    {
      step: 1,
      icon: Upload,
      title: "Upload Resume & Job Description",
      description: "Simply upload the candidate's resume and provide the job description. Our AI instantly begins processing the documents.",
      details: [
        "Secure file upload with encryption",
        "Support for PDF, DOC, and DOCX formats",
        "Automatic text extraction and parsing",
        "Job requirement analysis"
      ],
      color: "from-blue-500 to-cyan-500",
      bgColor: "bg-blue-50"
    },
    {
      step: 2,
      icon: Brain,
      title: "AI Analysis & Processing",
      description: "Advanced NLP algorithms analyze the resume, extract key information, and match skills with job requirements.",
      details: [
        "Skill identification and categorization",
        "Experience relevance scoring",
        "Education and certification verification",
        "Gap analysis and recommendations"
      ],
      color: "from-purple-500 to-pink-500",
      bgColor: "bg-purple-50"
    },
    {
      step: 3,
      icon: MessageSquare,
      title: "Intelligent Interview Simulation",
      description: "Personalized interview questions are generated based on the candidate's background and role requirements.",
      details: [
        "Adaptive question generation",
        "Real-time response evaluation",
        "Behavioral and technical assessment",
        "Follow-up question suggestions"
      ],
      color: "from-green-500 to-teal-500",
      bgColor: "bg-green-50"
    },
    {
      step: 4,
      icon: FileText,
      title: "Comprehensive Report Generation",
      description: "Receive detailed assessment reports with scores, insights, and actionable hiring recommendations.",
      details: [
        "Multi-dimensional scoring system",
        "Strengths and development areas",
        "Risk factor analysis",
        "Hiring confidence metrics"
      ],
      color: "from-orange-500 to-red-500",
      bgColor: "bg-orange-50"
    }
  ]

  return (
    <section id="how-it-works" className="py-24 bg-gradient-to-br from-slate-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <div className="text-center mb-16">
          <Badge className="mb-4 bg-purple-100 text-purple-700 hover:bg-purple-200 border-purple-200">
            <BarChart3 className="h-3 w-3 mr-1" />
            Simple Process
          </Badge>
          <h2 className="text-3xl sm:text-4xl font-bold text-slate-900 mb-4">
            How Our AI Platform
            <span className="block bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Transforms Hiring
            </span>
          </h2>
          <p className="text-xl text-slate-600 max-w-3xl mx-auto">
            From resume upload to final assessment report, our streamlined process delivers 
            comprehensive candidate insights in minutes, not hours.
          </p>
        </div>

        {/* Process steps */}
        <div className="space-y-12">
          {steps.map((step, index) => {
            const IconComponent = step.icon
            const isEven = index % 2 === 1
            
            return (
              <div key={index} className={`flex flex-col ${isEven ? 'lg:flex-row-reverse' : 'lg:flex-row'} items-center gap-8 lg:gap-16`}>
                {/* Content */}
                <div className="flex-1 space-y-6">
                  <div className="flex items-center space-x-4">
                    <div className={`w-12 h-12 rounded-full bg-gradient-to-r ${step.color} flex items-center justify-center text-white font-bold text-lg`}>
                      {step.step}
                    </div>
                    <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${step.color} flex items-center justify-center`}>
                      <IconComponent className="h-6 w-6 text-white" />
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="text-2xl font-bold text-slate-900 mb-3">
                      {step.title}
                    </h3>
                    <p className="text-lg text-slate-600 leading-relaxed mb-6">
                      {step.description}
                    </p>
                    
                    <ul className="space-y-3">
                      {step.details.map((detail, detailIndex) => (
                        <li key={detailIndex} className="flex items-center text-slate-700">
                          <CheckCircle className="h-5 w-5 text-green-500 mr-3 flex-shrink-0" />
                          {detail}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Visual */}
                <div className="flex-1">
                  <Card className={`${step.bgColor} border-none shadow-lg hover:shadow-xl transition-all duration-300`}>
                    <CardHeader className="text-center pb-4">
                      <div className={`w-16 h-16 rounded-full bg-gradient-to-r ${step.color} flex items-center justify-center mx-auto mb-4`}>
                        <IconComponent className="h-8 w-8 text-white" />
                      </div>
                      <CardTitle className="text-xl font-semibold text-slate-900">
                        Step {step.step}
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      {/* Mock interface elements based on step */}
                      {step.step === 1 && (
                        <div className="space-y-3">
                          <div className="bg-white rounded-lg p-4 border-2 border-dashed border-blue-300">
                            <div className="text-center">
                              <Upload className="h-8 w-8 text-blue-500 mx-auto mb-2" />
                              <p className="text-sm text-slate-600">Drop resume file here</p>
                            </div>
                          </div>
                          <div className="bg-white rounded-lg p-3">
                            <p className="text-xs text-slate-500 mb-1">Job Title</p>
                            <p className="text-sm font-medium">Senior Software Engineer</p>
                          </div>
                        </div>
                      )}
                      
                      {step.step === 2 && (
                        <div className="space-y-3">
                          <div className="bg-white rounded-lg p-3">
                            <div className="flex justify-between items-center mb-2">
                              <span className="text-xs text-slate-500">Processing</span>
                              <span className="text-xs text-blue-600">85%</span>
                            </div>
                            <div className="w-full bg-slate-200 rounded-full h-2">
                              <div className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full" style={{width: '85%'}}></div>
                            </div>
                          </div>
                          <div className="bg-white rounded-lg p-3 space-y-2">
                            <div className="flex items-center justify-between">
                              <span className="text-xs text-slate-600">Skills Extracted</span>
                              <CheckCircle className="h-4 w-4 text-green-500" />
                            </div>
                            <div className="flex items-center justify-between">
                              <span className="text-xs text-slate-600">Experience Analyzed</span>
                              <CheckCircle className="h-4 w-4 text-green-500" />
                            </div>
                          </div>
                        </div>
                      )}
                      
                      {step.step === 3 && (
                        <div className="space-y-3">
                          <div className="bg-white rounded-lg p-3">
                            <p className="text-xs text-slate-500 mb-1">Current Question</p>
                            <p className="text-sm font-medium">Tell me about your experience with React...</p>
                          </div>
                          <div className="bg-white rounded-lg p-3">
                            <div className="flex justify-between items-center">
                              <span className="text-xs text-slate-600">Progress</span>
                              <span className="text-xs text-purple-600">3/10</span>
                            </div>
                          </div>
                        </div>
                      )}
                      
                      {step.step === 4 && (
                        <div className="space-y-3">
                          <div className="bg-white rounded-lg p-3">
                            <div className="flex justify-between items-center mb-2">
                              <span className="text-xs text-slate-500">Overall Score</span>
                              <span className="text-lg font-bold text-green-600">92%</span>
                            </div>
                            <div className="text-xs text-slate-600">Strong Hire Recommendation</div>
                          </div>
                          <div className="bg-white rounded-lg p-3">
                            <p className="text-xs text-slate-500 mb-1">Key Strengths</p>
                            <div className="flex flex-wrap gap-1">
                              <Badge variant="secondary" className="text-xs">React Expert</Badge>
                              <Badge variant="secondary" className="text-xs">Team Lead</Badge>
                            </div>
                          </div>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                </div>

                {/* Arrow connector (except for last step) */}
                {index < steps.length - 1 && (
                  <div className="hidden lg:block absolute left-1/2 transform -translate-x-1/2 mt-32">
                    <ArrowRight className="h-8 w-8 text-slate-300" />
                  </div>
                )}
              </div>
            )
          })}
        </div>

        {/* CTA section */}
        <div className="mt-20 text-center">
          <div className="bg-white rounded-2xl p-8 md:p-12 shadow-lg border border-slate-200">
            <h3 className="text-2xl font-bold text-slate-900 mb-4">
              Ready to Transform Your Hiring Process?
            </h3>
            <p className="text-slate-600 mb-8 max-w-2xl mx-auto">
              Join thousands of companies already using our AI platform to make better, 
              faster, and more confident hiring decisions.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                size="lg" 
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8"
              >
                Start Free Trial
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              <Button 
                variant="outline" 
                size="lg" 
                className="border-slate-300 text-slate-700 hover:bg-slate-50 px-8"
              >
                Schedule Demo
              </Button>
            </div>
            
            {/* Trust indicators */}
            <div className="mt-8 pt-8 border-t border-slate-200">
              <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-8 text-sm text-slate-500">
                <div className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                  No credit card required
                </div>
                <div className="flex items-center">
                  <Clock className="h-4 w-4 text-blue-500 mr-2" />
                  Setup in 5 minutes
                </div>
                <div className="flex items-center">
                  <Users className="h-4 w-4 text-purple-500 mr-2" />
                  24/7 support included
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default HowItWorks

