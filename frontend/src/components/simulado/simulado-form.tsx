'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

interface SimuladoConfig {
  banca: string
  topico: string
  numQuestoes: number
  tempoLimite: number
  nivel: string
  materias: string[]
}

export function SimuladoForm() {
  const [config, setConfig] = useState<SimuladoConfig>({
    banca: 'CESPE',
    topico: '',
    numQuestoes: 20,
    tempoLimite: 60,
    nivel: 'intermediario',
    materias: []
  })

  const [isGenerating, setIsGenerating] = useState(false)

  const bancas = [
    { value: 'CESPE', label: 'CESPE/CEBRASPE' },
    { value: 'FGV', label: 'FGV' },
    { value: 'VUNESP', label: 'VUNESP' },
    { value: 'FCC', label: 'FCC' },
    { value: 'ESAF', label: 'ESAF' }
  ]

  const niveis = [
    { value: 'basico', label: 'Básico' },
    { value: 'intermediario', label: 'Intermediário' },
    { value: 'avancado', label: 'Avançado' }
  ]

  const materiasDisponiveis = [
    'Direito Constitucional',
    'Direito Administrativo',
    'Direito Penal',
    'Direito Civil',
    'Direito Processual Civil',
    'Direito Processual Penal',
    'Direito Tributário',
    'Direito do Trabalho',
    'Direito Previdenciário',
    'Administração Pública',
    'Contabilidade Pública',
    'Economia',
    'Português',
    'Raciocínio Lógico',
    'Informática'
  ]

  const handleMateriaChange = (materia: string) => {
    setConfig(prev => ({
      ...prev,
      materias: prev.materias.includes(materia)
        ? prev.materias.filter(m => m !== materia)
        : [...prev.materias, materia]
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsGenerating(true)
    
    try {
      // Importar o cliente da API
      const { apiClient } = await import('@/lib/api')
      
      // Criar simulado via API real
      const response = await apiClient.createSimulado({
        title: `Simulado ${config.banca} - ${config.materias.join(', ')}`,
        config: {
          banca: config.banca,
          subjects: config.materias,
          num_questions: config.numQuestoes,
          time_limit: config.tempoLimite,
          level: config.nivel
        },
        time_limit: config.tempoLimite,
        total_questions: config.numQuestoes
      })
      
      if (response.data) {
        // Redirecionar para a página do simulado
        window.location.href = `/simulado/${response.data.id}`
      } else {
        alert(response.error || 'Erro ao criar simulado')
      }
    } catch (error) {
      alert('Erro de conexão. Verifique se o backend está rodando.')
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Banca Organizadora
          </label>
          <select 
            className="w-full h-10 px-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            value={config.banca}
            onChange={(e) => setConfig(prev => ({ ...prev, banca: e.target.value }))}
          >
            {bancas.map(banca => (
              <option key={banca.value} value={banca.value}>
                {banca.label}
              </option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Nível de Dificuldade
          </label>
          <select 
            className="w-full h-10 px-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            value={config.nivel}
            onChange={(e) => setConfig(prev => ({ ...prev, nivel: e.target.value }))}
          >
            {niveis.map(nivel => (
              <option key={nivel.value} value={nivel.value}>
                {nivel.label}
              </option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Tópico Específico (opcional)
          </label>
          <Input 
            placeholder="Ex: Controle de Constitucionalidade"
            value={config.topico}
            onChange={(e) => setConfig(prev => ({ ...prev, topico: e.target.value }))}
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Número de Questões
          </label>
          <Input 
            type="number" 
            min="5"
            max="100"
            value={config.numQuestoes}
            onChange={(e) => setConfig(prev => ({ ...prev, numQuestoes: parseInt(e.target.value) || 20 }))}
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Tempo Limite (minutos)
          </label>
          <Input 
            type="number" 
            min="15"
            max="300"
            value={config.tempoLimite}
            onChange={(e) => setConfig(prev => ({ ...prev, tempoLimite: parseInt(e.target.value) || 60 }))}
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Matérias (selecione pelo menos uma)
        </label>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {materiasDisponiveis.map(materia => (
            <label key={materia} className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                checked={config.materias.includes(materia)}
                onChange={() => handleMateriaChange(materia)}
                className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />
              <span className="text-sm text-gray-700">{materia}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-medium text-blue-900 mb-2">📋 Resumo do Simulado</h4>
        <div className="text-sm text-blue-800 space-y-1">
          <p><strong>Banca:</strong> {bancas.find(b => b.value === config.banca)?.label}</p>
          <p><strong>Questões:</strong> {config.numQuestoes}</p>
          <p><strong>Tempo:</strong> {config.tempoLimite} minutos</p>
          <p><strong>Matérias:</strong> {config.materias.length > 0 ? config.materias.join(', ') : 'Nenhuma selecionada'}</p>
        </div>
      </div>
      
      <Button 
        type="submit" 
        className="w-full" 
        size="lg"
        disabled={isGenerating || config.materias.length === 0}
      >
        {isGenerating ? 'Gerando Simulado...' : '🚀 Gerar Simulado'}
      </Button>
    </form>
  )
}
