'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { generateAPI, userAPI, type AdVariation, type UsageStats } from '@/lib/api'

export default function DashboardPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [usage, setUsage] = useState<UsageStats | null>(null)
  const [variations, setVariations] = useState<AdVariation[]>([])
  
  // Form state
  const [url, setUrl] = useState('')
  const [productName, setProductName] = useState('')
  const [valueProp1, setValueProp1] = useState('')
  const [valueProp2, setValueProp2] = useState('')
  const [valueProp3, setValueProp3] = useState('')
  const [brandVoice, setBrandVoice] = useState('Professional')

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/auth/login')
      return
    }
    loadUsage()
  }, [router])

  const loadUsage = async () => {
    try {
      const stats = await userAPI.getUsage()
      setUsage(stats)
    } catch (err) {
      console.error('Failed to load usage:', err)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    router.push('/auth/login')
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    setVariations([])

    const valueProps = [valueProp1, valueProp2, valueProp3].filter(v => v.trim())
    
    if (valueProps.length === 0) {
      setError('Please provide at least one value proposition')
      setLoading(false)
      return
    }

    try {
      const response = await generateAPI.generate({
        url,
        product_name: productName,
        value_props: valueProps,
        brand_voice: brandVoice,
      })
      setVariations(response.variations)
      await loadUsage() // Refresh usage stats
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Generation failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold tracking-tight text-gray-900">
            Contextual Ad Engine
          </h1>
          <div className="flex items-center gap-4">
            {usage && (
              <div className="text-sm text-gray-600">
                <span className="font-semibold">{usage.remaining}</span> / {usage.limit} generations remaining
                {!usage.is_pro && (
                  <span className="ml-2 text-primary-600 font-medium cursor-pointer hover:underline">
                    Upgrade to Pro
                  </span>
                )}
              </div>
            )}
            <button
              onClick={handleLogout}
              className="text-sm text-gray-600 hover:text-gray-900"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Generate Ad Copy</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="url" className="block text-sm font-medium text-gray-700">
                  Landing Page URL
                </label>
                <input
                  type="url"
                  id="url"
                  required
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border"
                  placeholder="https://example.com/product"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                />
              </div>

              <div>
                <label htmlFor="productName" className="block text-sm font-medium text-gray-700">
                  Product Name
                </label>
                <input
                  type="text"
                  id="productName"
                  required
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border"
                  placeholder="My Awesome Product"
                  value={productName}
                  onChange={(e) => setProductName(e.target.value)}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Value Propositions
                </label>
                <input
                  type="text"
                  className="mb-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border"
                  placeholder="Value proposition 1"
                  value={valueProp1}
                  onChange={(e) => setValueProp1(e.target.value)}
                />
                <input
                  type="text"
                  className="mb-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border"
                  placeholder="Value proposition 2"
                  value={valueProp2}
                  onChange={(e) => setValueProp2(e.target.value)}
                />
                <input
                  type="text"
                  className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border"
                  placeholder="Value proposition 3"
                  value={valueProp3}
                  onChange={(e) => setValueProp3(e.target.value)}
                />
              </div>

              <div>
                <label htmlFor="brandVoice" className="block text-sm font-medium text-gray-700">
                  Brand Voice
                </label>
                <select
                  id="brandVoice"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border"
                  value={brandVoice}
                  onChange={(e) => setBrandVoice(e.target.value)}
                >
                  <option>Professional</option>
                  <option>Playful</option>
                  <option>Urgent</option>
                  <option>Friendly</option>
                  <option>Authoritative</option>
                </select>
              </div>

              {error && (
                <div className="rounded-md bg-red-50 p-4">
                  <p className="text-sm text-red-800">{error}</p>
                </div>
              )}

              <button
                type="submit"
                disabled={loading || (usage && usage.remaining <= 0)}
                className="w-full flex justify-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Generating...' : 'Generate Ad Copy'}
              </button>
            </form>
          </div>

          {/* Results */}
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Generated Variations</h2>
            {variations.length === 0 ? (
              <p className="text-gray-500 text-center py-8">
                Your generated ad copy variations will appear here
              </p>
            ) : (
              <div className="space-y-4">
                {variations.map((variation, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-semibold text-gray-900">Variation {index + 1}</h3>
                      <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                        {variation.strategy}
                      </span>
                    </div>
                    <div className="space-y-2">
                      <div>
                        <p className="text-xs text-gray-500 uppercase">Headline</p>
                        <p className="text-sm font-medium text-gray-900">{variation.headline}</p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500 uppercase">Body</p>
                        <p className="text-sm text-gray-700">{variation.body}</p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500 uppercase">CTA</p>
                        <p className="text-sm font-semibold text-primary-600">{variation.cta}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
