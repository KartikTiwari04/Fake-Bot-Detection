import React, { useState } from 'react';
import { AlertCircle, CheckCircle, Loader, Brain, User, BarChart3, Info } from 'lucide-react';

export default function AITextDetector() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const API_URL = 'http://localhost:8000'; // Change this to your backend URL

  const analyzeText = async () => {
    if (!text.trim()) {
      setError('Please enter some text to analyze');
      return;
    }

    if (text.length < 10) {
      setError('Text must be at least 10 characters long');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/detect`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to analyze text');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Failed to connect to the API. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const examples = [
    {
      label: 'Human-like',
      text: "omg i cant believe what happened today!! went to the store and they were out of my fav snacks... like seriously? anyway grabbed some random stuff and headed home. btw did u see that show last night??"
    },
    {
      label: 'AI-like',
      text: "Artificial intelligence has revolutionized numerous industries through advanced machine learning algorithms. It's important to note that AI systems process vast amounts of data to generate insights. Furthermore, these technologies continue to evolve rapidly, presenting both opportunities and challenges for society."
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-6">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center items-center gap-3 mb-4">
            <Brain className="w-12 h-12 text-blue-600" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              AI Text Detector
            </h1>
          </div>
          <p className="text-gray-600 text-lg">
            Detect whether text is written by a human or AI using machine learning
          </p>
        </div>

        {/* Main Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
          {/* Text Input */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Enter Text to Analyze (minimum 20 words, 50+ recommended)
            </label>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Paste or type the text you want to analyze... For best results, use 50+ words with complete sentences."
              className="w-full h-48 p-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors resize-none"
            />
            <div className="flex justify-between items-center mt-2">
              <span className={`text-sm ${text.split(/\s+/).filter(w => w).length < 20 ? 'text-red-500 font-semibold' : 'text-gray-500'}`}>
                {text.length} characters | {text.split(/\s+/).filter(w => w).length} words
                {text.split(/\s+/).filter(w => w).length < 20 && ' (Need 20+ words)'}
              </span>
              <button
                onClick={() => setText('')}
                className="text-sm text-gray-500 hover:text-gray-700 underline"
              >
                Clear
              </button>
            </div>
          </div>

          {/* Example Texts */}
          <div className="mb-6">
            <p className="text-sm font-semibold text-gray-700 mb-2">Try these examples (50+ words each):</p>
            <div className="flex gap-3 flex-wrap">
              {examples.map((example, idx) => (
                <button
                  key={idx}
                  onClick={() => setText(example.text)}
                  className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm transition-colors"
                >
                  {example.label}
                </button>
              ))}
            </div>
            <p className="text-xs text-gray-500 mt-2">
              💡 <strong>Best for:</strong> Paragraphs, essays, articles, blog posts, emails (50+ words)
            </p>
            <p className="text-xs text-gray-500">
              ❌ <strong>Not reliable for:</strong> Short phrases, greetings, simple questions (under 20 words)
            </p>
          </div>

          {/* Analyze Button */}
          <button
            onClick={analyzeText}
            disabled={loading || !text.trim()}
            className="w-full py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-[1.02] active:scale-[0.98] flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader className="w-5 h-5 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Brain className="w-5 h-5" />
                Analyze Text
              </>
            )}
          </button>

          {/* Error Message */}
          {error && (
            <div className="mt-6 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-red-800">Error</p>
                <p className="text-red-600 text-sm">{error}</p>
              </div>
            </div>
          )}
        </div>

        {/* Results */}
        {result && (
          <div className="space-y-6">
            {/* Main Result Card */}
            <div className={`bg-white rounded-2xl shadow-xl p-8 border-l-8 ${
              result.is_ai_generated ? 'border-purple-500' : 'border-green-500'
            }`}>
              <div className="flex items-start justify-between mb-6">
                <div className="flex items-center gap-4">
                  {result.is_ai_generated ? (
                    <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center">
                      <Brain className="w-8 h-8 text-purple-600" />
                    </div>
                  ) : (
                    <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
                      <User className="w-8 h-8 text-green-600" />
                    </div>
                  )}
                  <div>
                    <h2 className="text-2xl font-bold text-gray-800">
                      {result.is_ai_generated ? 'AI-Generated' : 'Human-Written'}
                    </h2>
                    <p className="text-gray-600">Detection Result</p>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-3xl font-bold text-gray-800">
                    {(result.confidence * 100).toFixed(1)}%
                  </div>
                  <p className="text-sm text-gray-600">Confidence</p>
                </div>
              </div>

              {/* Probability Bars */}
              <div className="space-y-4 mb-6">
                <div>
                  <div className="flex justify-between mb-1">
                    <span className="text-sm font-medium text-purple-700 flex items-center gap-1">
                      <Brain className="w-4 h-4" />
                      AI Probability
                    </span>
                    <span className="text-sm font-semibold text-purple-700">
                      {(result.ai_probability * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className="bg-gradient-to-r from-purple-500 to-purple-600 h-3 rounded-full transition-all duration-500"
                      style={{ width: `${result.ai_probability * 100}%` }}
                    />
                  </div>
                </div>

                <div>
                  <div className="flex justify-between mb-1">
                    <span className="text-sm font-medium text-green-700 flex items-center gap-1">
                      <User className="w-4 h-4" />
                      Human Probability
                    </span>
                    <span className="text-sm font-semibold text-green-700">
                      {(result.human_probability * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className="bg-gradient-to-r from-green-500 to-green-600 h-3 rounded-full transition-all duration-500"
                      style={{ width: `${result.human_probability * 100}%` }}
                    />
                  </div>
                </div>
              </div>

              {/* Explanation */}
              <div className="bg-blue-50 rounded-xl p-4 border border-blue-200">
                <div className="flex items-start gap-3">
                  <Info className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <h3 className="font-semibold text-blue-900 mb-1">Analysis</h3>
                    <p className="text-blue-800 text-sm">{result.explanation}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Features Card */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <div className="flex items-center gap-2 mb-6">
                <BarChart3 className="w-6 h-6 text-gray-700" />
                <h3 className="text-xl font-bold text-gray-800">Text Features</h3>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-gray-50 rounded-lg p-4">
                  <p className="text-sm text-gray-600 mb-1">Words</p>
                  <p className="text-2xl font-bold text-gray-800">{result.features.word_count}</p>
                </div>
                <div className="bg-gray-50 rounded-lg p-4">
                  <p className="text-sm text-gray-600 mb-1">Sentences</p>
                  <p className="text-2xl font-bold text-gray-800">{result.features.sentence_count}</p>
                </div>
                <div className="bg-gray-50 rounded-lg p-4">
                  <p className="text-sm text-gray-600 mb-1">Avg Word Length</p>
                  <p className="text-2xl font-bold text-gray-800">{result.features.avg_word_length.toFixed(1)}</p>
                </div>
                <div className="bg-gray-50 rounded-lg p-4">
                  <p className="text-sm text-gray-600 mb-1">Lexical Diversity</p>
                  <p className="text-2xl font-bold text-gray-800">{(result.features.lexical_diversity * 100).toFixed(0)}%</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-8 text-sm text-gray-500">
          <p>Powered by Machine Learning • Built with FastAPI & React</p>
        </div>
      </div>
    </div>
  );
}