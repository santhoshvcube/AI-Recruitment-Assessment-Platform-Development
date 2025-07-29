import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  FileText, 
  MessageSquare, 
  BarChart3, 
  Shield, 
  Brain,
  Users,
  Clock,
  Target,
  CheckCircle,
  Zap,
  Lock,
  TrendingUp
} from 'lucide-react'

const Features = () => {
  const features = [
    {
      icon: FileText,
      title: "Advanced Resume Analysis",
      description: "AI-powered extraction and analysis of candidate skills, experience, and qualifications with 95% accuracy.",
      benefits: ["Automated skill identification", "Experience relevance scoring", "Education verification", "Contact extraction"],
      color: "from-blue-500 to-cyan-500"
    },
    {
      icon: MessageSquare,
      title: "Intelligent Interview Simulation",
      description: "Adaptive questioning system that generates personalized interview questions based on job requirements.",
      benefits: ["Dynamic question generation", "Real-time response analysis", "Behavioral assessment", "Technical evaluation"],
      color: "from-purple-500 to-pink-500"
    },
    {
      icon: BarChart3,
      title: "Comprehensive Assessment Reports",
      description: "Detailed evaluation reports with actionable insights and data-driven hiring recommendations.",
      benefits: ["Multi-dimensional scoring", "Risk factor analysis", "Development recommendations", "Hiring confidence metrics"],
      color: "from-green-500 to-teal-500"
    },
    {
      icon: Shield,
      title: "Enterprise Security",
      description: "Bank-grade security with end-to-end encryption ensuring complete confidentiality of candidate data.",
      benefits: ["Data encryption", "Access control", "Audit trails", "GDPR compliance"],
      color: "from-red-500 to-orange-500"
    },
    {
      icon: Brain,
      title: "Machine Learning Insights",
      description: "Continuously improving AI models that learn from assessment patterns to enhance accuracy.",
      benefits: ["Predictive analytics", "Pattern recognition", "Performance optimization", "Bias reduction"],
      color: "from-indigo-500 to-purple-500"
    },
    {
      icon: Users,
      title: "Cultural Fit Analysis",
      description: "Evaluate candidate alignment with company culture and team dynamics for better hiring decisions.",
      benefits: ["Personality assessment", "Team compatibility", "Value alignment", "Communication style analysis"],
      color: "from-yellow-500 to-orange-500"
    }
  ]

  return (
    <section id="features" className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <div className="text-center mb-16">
          <Badge className="mb-4 bg-blue-100 text-blue-700 hover:bg-blue-200 border-blue-200">
            <Zap className="h-3 w-3 mr-1" />
            Powerful Features
          </Badge>
          <h2 className="text-3xl sm:text-4xl font-bold text-slate-900 mb-4">
            Everything You Need for
            <span className="block bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Intelligent Hiring
            </span>
          </h2>
          <p className="text-xl text-slate-600 max-w-3xl mx-auto">
            Our comprehensive AI platform provides all the tools you need to make data-driven hiring decisions 
            with confidence and efficiency.
          </p>
        </div>

        {/* Features grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          {features.map((feature, index) => {
            const IconComponent = feature.icon
            return (
              <Card key={index} className="group hover:shadow-xl transition-all duration-300 border-slate-200 hover:border-slate-300">
                <CardHeader className="pb-4">
                  <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${feature.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}>
                    <IconComponent className="h-6 w-6 text-white" />
                  </div>
                  <CardTitle className="text-xl font-semibold text-slate-900 group-hover:text-blue-600 transition-colors">
                    {feature.title}
                  </CardTitle>
                  <CardDescription className="text-slate-600 leading-relaxed">
                    {feature.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {feature.benefits.map((benefit, benefitIndex) => (
                      <li key={benefitIndex} className="flex items-center text-sm text-slate-600">
                        <CheckCircle className="h-4 w-4 text-green-500 mr-2 flex-shrink-0" />
                        {benefit}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )
          })}
        </div>

        {/* Additional benefits */}
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-8 md:p-12">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
            <div>
              <h3 className="text-2xl font-bold text-slate-900 mb-4">
                Why Choose Our AI Platform?
              </h3>
              <p className="text-slate-600 mb-6 leading-relaxed">
                Our platform combines cutting-edge AI technology with practical recruitment needs, 
                delivering measurable improvements in hiring quality and efficiency.
              </p>
              <div className="space-y-4">
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mr-3">
                    <Clock className="h-4 w-4 text-green-600" />
                  </div>
                  <span className="text-slate-700">75% reduction in screening time</span>
                </div>
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                    <Target className="h-4 w-4 text-blue-600" />
                  </div>
                  <span className="text-slate-700">95% accuracy in candidate assessment</span>
                </div>
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center mr-3">
                    <TrendingUp className="h-4 w-4 text-purple-600" />
                  </div>
                  <span className="text-slate-700">40% improvement in hire quality</span>
                </div>
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center mr-3">
                    <Lock className="h-4 w-4 text-red-600" />
                  </div>
                  <span className="text-slate-700">Enterprise-grade security & compliance</span>
                </div>
              </div>
            </div>
            <div className="relative">
              <div className="bg-white rounded-xl p-6 shadow-lg">
                <div className="flex items-center justify-between mb-4">
                  <h4 className="font-semibold text-slate-900">Assessment Progress</h4>
                  <Badge className="bg-green-100 text-green-700">Completed</Badge>
                </div>
                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-slate-600">Resume Analysis</span>
                      <span className="text-slate-900 font-medium">98%</span>
                    </div>
                    <div className="w-full bg-slate-200 rounded-full h-2">
                      <div className="bg-gradient-to-r from-blue-500 to-cyan-500 h-2 rounded-full" style={{width: '98%'}}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-slate-600">Interview Performance</span>
                      <span className="text-slate-900 font-medium">92%</span>
                    </div>
                    <div className="w-full bg-slate-200 rounded-full h-2">
                      <div className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full" style={{width: '92%'}}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-slate-600">Cultural Fit</span>
                      <span className="text-slate-900 font-medium">89%</span>
                    </div>
                    <div className="w-full bg-slate-200 rounded-full h-2">
                      <div className="bg-gradient-to-r from-green-500 to-teal-500 h-2 rounded-full" style={{width: '89%'}}></div>
                    </div>
                  </div>
                </div>
                <div className="mt-4 pt-4 border-t border-slate-200">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium text-slate-900">Overall Score</span>
                    <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">93%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Features

