import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ArrowRight, Zap, Brain, DollarSign, Shield, BarChart3, Users, Sparkles } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-20 pb-16">
          <div className="text-center">
            <Badge variant="secondary" className="mb-4">
              <Sparkles className="w-3 h-3 mr-1" />
              AI-Powered Optimization
            </Badge>
            
            <h1 className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-6xl">
              Optimize Your AI Prompts
              <span className="block text-blue-600 dark:text-blue-400">
                Save 45%+ on Tokens
              </span>
            </h1>
            
            <p className="mt-6 text-lg leading-8 text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Build the world's most effective AI prompt optimization platform. Enhance result quality 
              while aggressively reducing token costs across GPT-4, Claude, and Gemini.
            </p>
            
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Button size="lg" asChild>
                <Link href="/dashboard">
                  Get Started Free
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
              <Button variant="outline" size="lg" asChild>
                <Link href="/demo">
                  Try Demo
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-white dark:bg-slate-900">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
              Why Choose AI Prompt Optimizer?
            </h2>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">
              Advanced features designed to maximize your AI efficiency and ROI
            </p>
          </div>

          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            <Card>
              <CardHeader>
                <Zap className="h-8 w-8 text-blue-600" />
                <CardTitle>Smart Token Reduction</CardTitle>
                <CardDescription>
                  Automatically reduce token usage by up to 45% while maintaining or improving output quality
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <Brain className="h-8 w-8 text-green-600" />
                <CardTitle>Multi-Model Support</CardTitle>
                <CardDescription>
                  Optimize prompts for GPT-4, Claude, Gemini, and custom models with intelligent adaptation
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <DollarSign className="h-8 w-8 text-yellow-600" />
                <CardTitle>Cost Calculator</CardTitle>
                <CardDescription>
                  Real-time token counting and cost analysis to optimize your AI spending
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <Shield className="h-8 w-8 text-purple-600" />
                <CardTitle>Enterprise Security</CardTitle>
                <CardDescription>
                  SOC 2 compliant with enterprise-grade security and team collaboration features
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <BarChart3 className="h-8 w-8 text-red-600" />
                <CardTitle>Analytics Dashboard</CardTitle>
                <CardDescription>
                  Track performance, ROI, and optimization metrics with detailed insights
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <Users className="h-8 w-8 text-indigo-600" />
                <CardTitle>Team Collaboration</CardTitle>
                <CardDescription>
                  Share prompt libraries, templates, and optimization strategies across your team
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-blue-600 dark:bg-blue-700">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Ready to Optimize Your AI Workflow?
          </h2>
          <p className="mt-4 text-lg text-blue-100">
            Join thousands of developers and teams already saving on AI costs
          </p>
          <div className="mt-8">
            <Button size="lg" variant="secondary" asChild>
              <Link href="/register">
                Start Free Trial
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  )
} 