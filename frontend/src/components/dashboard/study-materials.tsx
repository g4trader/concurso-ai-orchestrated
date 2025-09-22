'use client'

import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import Link from 'next/link'

interface StudyMaterial {
  id: string
  title: string
  type: 'video' | 'article' | 'quiz' | 'document'
  subject: string
  duration?: string
  difficulty: 'basico' | 'intermediario' | 'avancado'
  description: string
}

const studyMaterials: StudyMaterial[] = [
  {
    id: '1',
    title: 'Direito Constitucional - Princípios Fundamentais',
    type: 'video',
    subject: 'Direito Constitucional',
    duration: '45min',
    difficulty: 'basico',
    description: 'Aula completa sobre os princípios fundamentais da Constituição Federal'
  },
  {
    id: '2',
    title: 'Administração Pública - Princípios Constitucionais',
    type: 'article',
    subject: 'Direito Administrativo',
    duration: '20min',
    difficulty: 'intermediario',
    description: 'Artigo detalhado sobre os princípios da administração pública'
  },
  {
    id: '3',
    title: 'Português - Concordância Verbal',
    type: 'quiz',
    subject: 'Português',
    duration: '15min',
    difficulty: 'basico',
    description: 'Quiz interativo sobre concordância verbal'
  },
  {
    id: '4',
    title: 'Raciocínio Lógico - Lógica Proposicional',
    type: 'video',
    subject: 'Raciocínio Lógico',
    duration: '60min',
    difficulty: 'avancado',
    description: 'Aula avançada sobre lógica proposicional e tabelas verdade'
  },
  {
    id: '5',
    title: 'Informática - Segurança da Informação',
    type: 'document',
    subject: 'Informática',
    duration: '30min',
    difficulty: 'intermediario',
    description: 'Material completo sobre segurança da informação'
  }
]

const getTypeIcon = (type: string) => {
  switch (type) {
    case 'video': return '🎥'
    case 'article': return '📄'
    case 'quiz': return '🧩'
    case 'document': return '📚'
    default: return '📖'
  }
}

const getDifficultyColor = (difficulty: string) => {
  switch (difficulty) {
    case 'basico': return 'bg-green-100 text-green-800'
    case 'intermediario': return 'bg-yellow-100 text-yellow-800'
    case 'avancado': return 'bg-red-100 text-red-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

export function StudyMaterials() {
  return (
    <Card className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">Materiais de Estudo</h3>
        <Button variant="outline" size="sm">
          Ver todos
        </Button>
      </div>
      
      <div className="space-y-3">
        {studyMaterials.slice(0, 4).map((material) => (
          <div key={material.id} className="border rounded-lg p-4 hover:bg-gray-50 transition-colors">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-lg">{getTypeIcon(material.type)}</span>
                  <h4 className="font-medium text-gray-900">{material.title}</h4>
                </div>
                <p className="text-sm text-gray-600 mb-2">{material.description}</p>
                <div className="flex items-center gap-3 text-xs text-gray-500">
                  <span>{material.subject}</span>
                  {material.duration && <span>• {material.duration}</span>}
                  <span className={`px-2 py-1 rounded ${getDifficultyColor(material.difficulty)}`}>
                    {material.difficulty}
                  </span>
                </div>
              </div>
              <Button size="sm" variant="outline">
                Acessar
              </Button>
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-4 pt-4 border-t border-gray-200">
        <div className="grid grid-cols-2 gap-4">
          <Link href="/materiais">
            <div className="p-3 border rounded-lg hover:bg-gray-50 cursor-pointer transition-colors text-center">
              <div className="text-2xl mb-1">📚</div>
              <p className="text-sm font-medium">Biblioteca</p>
            </div>
          </Link>
          <Link href="/quiz-rapido">
            <div className="p-3 border rounded-lg hover:bg-gray-50 cursor-pointer transition-colors text-center">
              <div className="text-2xl mb-1">⚡</div>
              <p className="text-sm font-medium">Quiz Rápido</p>
            </div>
          </Link>
        </div>
      </div>
    </Card>
  )
}
