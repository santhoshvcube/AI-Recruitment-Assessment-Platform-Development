import { Link } from 'react-router-dom'
import { 
  Brain, 
  Mail, 
  Phone, 
  MapPin,
  Twitter,
  Linkedin,
  Github,
  Heart
} from 'lucide-react'

const Footer = () => {
  return (
    <footer className="bg-slate-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-2 rounded-lg">
                <Brain className="h-6 w-6 text-white" />
              </div>
              <span className="text-xl font-bold">AI Interview</span>
            </div>
            <p className="text-slate-300 leading-relaxed">
              Revolutionizing recruitment with AI-powered candidate assessment and intelligent interview simulation.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-slate-400 hover:text-white transition-colors">
                <Twitter className="h-5 w-5" />
              </a>
              <a href="#" className="text-slate-400 hover:text-white transition-colors">
                <Linkedin className="h-5 w-5" />
              </a>
              <a href="#" className="text-slate-400 hover:text-white transition-colors">
                <Github className="h-5 w-5" />
              </a>
            </div>
          </div>

          {/* Product */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Product</h3>
            <ul className="space-y-2">
              <li>
                <a href="#features" className="text-slate-300 hover:text-white transition-colors">
                  Features
                </a>
              </li>
              <li>
                <a href="#how-it-works" className="text-slate-300 hover:text-white transition-colors">
                  How It Works
                </a>
              </li>
              <li>
                <a href="#" className="text-slate-300 hover:text-white transition-colors">
                  Pricing
                </a>
              </li>
              <li>
                <a href="#" className="text-slate-300 hover:text-white transition-colors">
                  API Documentation
                </a>
              </li>
              <li>
                <a href="#" className="text-slate-300 hover:text-white transition-colors">
                  Integrations
                </a>
              </li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Company</h3>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-slate-300 hover:text-white transition-colors">
                  About Us
                </a>
              </li>
              <li>
                <a href="#" className="text-slate-300 hover:text-white transition-colors">
                  Careers
                </a>
              </li>
              <li>
                <a href="#" className="text-slate-300 hover:text-white transition-colors">
                  Blog
                </a>
              </li>
              <li>
                <a href="#" className="text-slate-300 hover:text-white transition-colors">
                  Press
                </a>
              </li>
              <li>
                <a href="#" className="text-slate-300 hover:text-white transition-colors">
                  Partners
                </a>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Support</h3>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-slate-300 hover:text-white transition-colors">
                  Help Center
                </a>
              </li>
              <li>
                <a href="#" className="text-slate-300 hover:text-white transition-colors">
                  Contact Support
                </a>
              </li>
              <li>
                <a href="#" className="text-slate-300 hover:text-white transition-colors">
                  Status Page
                </a>
              </li>
              <li>
                <a href="#" className="text-slate-300 hover:text-white transition-colors">
                  Security
                </a>
              </li>
              <li>
                <a href="#" className="text-slate-300 hover:text-white transition-colors">
                  Privacy Policy
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Contact Info */}
        <div className="border-t border-slate-800 mt-8 pt-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="flex items-center space-x-3">
              <Mail className="h-5 w-5 text-blue-400" />
              <span className="text-slate-300">contact@aiinterview.com</span>
            </div>
            <div className="flex items-center space-x-3">
              <Phone className="h-5 w-5 text-blue-400" />
              <span className="text-slate-300">+1 (555) 123-4567</span>
            </div>
            <div className="flex items-center space-x-3">
              <MapPin className="h-5 w-5 text-blue-400" />
              <span className="text-slate-300">San Francisco, CA</span>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-slate-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
          <div className="text-slate-400 text-sm">
            © 2024 AI Interview Platform. All rights reserved.
          </div>
          <div className="flex items-center space-x-1 text-slate-400 text-sm mt-4 md:mt-0">
            <span>Made with</span>
            <Heart className="h-4 w-4 text-red-500" />
            <span>for better hiring</span>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer

