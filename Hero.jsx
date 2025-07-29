import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  Brain, 
  ArrowRight, 
  Star, 
  CheckCircle,
  Users,
  BarChart3,
  Shield
} from 'lucide-react'
import { useNavigate } from 'react-router-dom';

const Hero = () => {
  const navigate = useNavigate();

  const handleStartFreeAssessment = () => {
    navigate('/login');
  };

  return (
    <section className="relative overflow-hidden bg-gradient-to-br from-slate-50 to-blue-50 pt-20 pb-32">
      {/* Background decoration */}
      <div className="absolute inset-0 bg-grid-slate-100 [mask-image:linear-gradient(0deg,white,rgba(255,255,255,0.6))] -z-10" />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          {/* Badge */}
          <Badge className="mb-6 bg-blue-100 text-blue-700 hover:bg-blue-200 border-blue-200">
            <Star className="h-3 w-3 mr-1" />
            AI-Powered Recruitment Platform
          </Badge>

          {/* Main heading */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-slate-900 mb-6">
            Revolutionize Your
            <span className="block bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Hiring Process
            </span>
            with AI Intelligence
          </h1>

          {/* Subtitle */}
          <p className="text-xl text-slate-600 mb-8 max-w-3xl mx-auto leading-relaxed">
            Transform candidate assessment with our advanced AI platform. Analyze resumes, conduct intelligent interviews, 
            and generate comprehensive reports with unmatched accuracy and efficiency.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
            <Button 
              size="lg" 
              className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-3 text-lg"
              onClick={handleStartFreeAssessment}
            >
              Start Free Assessment
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button 
              variant="outline" 
              size="lg" 
              className="border-slate-300 text-slate-700 hover:bg-slate-50 px-8 py-3 text-lg"
            >
              Watch Demo
            </Button>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 max-w-2xl mx-auto mb-16">
            <div className="text-center">
              <div className="text-3xl font-bold text-slate-900 mb-2">95%</div>
              <div className="text-slate-600">Accuracy Rate</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-slate-900 mb-2">10k+</div>
              <div className="text-slate-600">Assessments Completed</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-slate-900 mb-2">75%</div>
              <div className="text-slate-600">Time Saved</div>
            </div>
          </div>

          {/* Feature highlights */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            <div className="bg-white/60 backdrop-blur-sm rounded-xl p-6 border border-slate-200 hover:shadow-lg transition-all duration-300">
              <div className="bg-gradient-to-r from-blue-500 to-purple-500 w-12 h-12 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <Brain className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-slate-900 mb-2">AI-Powered Analysis</h3>
              <p className="text-slate-600 text-sm">
                Advanced NLP algorithms analyze resumes and extract key insights with unprecedented accuracy.
              </p>
            </div>

            <div className="bg-white/60 backdrop-blur-sm rounded-xl p-6 border border-slate-200 hover:shadow-lg transition-all duration-300">
              <div className="bg-gradient-to-r from-green-500 to-teal-500 w-12 h-12 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <Users className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-slate-900 mb-2">Smart Interviews</h3>
              <p className="text-slate-600 text-sm">
                Adaptive interview questions tailored to each candidate's background and the specific role.
              </p>
            </div>

            <div className="bg-white/60 backdrop-blur-sm rounded-xl p-6 border border-slate-200 hover:shadow-lg transition-all duration-300">
              <div className="bg-gradient-to-r from-orange-500 to-red-500 w-12 h-12 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <BarChart3 className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-slate-900 mb-2">Detailed Reports</h3>
              <p className="text-slate-600 text-sm">
                Comprehensive assessment reports with actionable insights and hiring recommendations.
              </p>
            </div>
          </div>

          {/* Trust indicators */}
          <div className="mt-16 pt-8 border-t border-slate-200">
            <p className="text-slate-500 text-sm mb-6">Trusted by leading companies worldwide</p>
            <div className="flex items-center justify-center space-x-8 opacity-60">
              <div className="text-2xl font-bold text-slate-400">TechCorp</div>
              <div className="text-2xl font-bold text-slate-400">InnovateLab</div>
              <div className="text-2xl font-bold text-slate-400">FutureWorks</div>
              <div className="text-2xl font-bold text-slate-400">NextGen</div>
            </div>
          </div>
        </div>
      </div>

      {/* Floating elements */}
      <div className="absolute top-20 left-10 w-20 h-20 bg-blue-200 rounded-full opacity-20 animate-pulse" />
      <div className="absolute top-40 right-20 w-16 h-16 bg-purple-200 rounded-full opacity-20 animate-pulse delay-1000" />
      <div className="absolute bottom-20 left-1/4 w-12 h-12 bg-green-200 rounded-full opacity-20 animate-pulse delay-2000" />
    </section>
  )
}

export default Hero


