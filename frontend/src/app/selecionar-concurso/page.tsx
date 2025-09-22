'use client';

import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { 
  Search, 
  Filter, 
  Calendar, 
  Users, 
  DollarSign,
  FileText,
  Brain,
  ExternalLink,
  CheckCircle,
  Clock,
  GraduationCap
} from 'lucide-react';

interface Concurso {
  id: string;
  titulo: string;
  orgao: string;
  banca: string;
  vagas: number;
  cargos: string[];
  salario: string;
  inscricoes: string;
  prova: string;
  edital_url: string;
  status: string;
  nivel: string;
  fonte: string;
  fonte_nome: string;
  fonte_url: string;
}

interface Filtros {
  banca: string;
  orgao: string;
  nivel: string;
  status: string;
}

export default function SelecionarConcursoPage() {
  const [concursos, setConcursos] = useState<Concurso[]>([]);
  const [concursosFiltrados, setConcursosFiltrados] = useState<Concurso[]>([]);
  const [loading, setLoading] = useState(true);
  const [analisando, setAnalisando] = useState<string | null>(null);
  const [filtros, setFiltros] = useState<Filtros>({
    banca: '',
    orgao: '',
    nivel: '',
    status: ''
  });
  const [busca, setBusca] = useState('');

  const API_BASE_URL = 'http://localhost:8002';

  useEffect(() => {
    carregarConcursos();
  }, []);

  useEffect(() => {
    filtrarConcursos();
  }, [concursos, filtros, busca]);

  const carregarConcursos = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/editais/concursos`);
      
      if (!response.ok) {
        throw new Error('Erro ao carregar concursos');
      }
      
      const data = await response.json();
      setConcursos(data);
    } catch (error) {
      console.error('Erro ao carregar concursos:', error);
    } finally {
      setLoading(false);
    }
  };

  const filtrarConcursos = () => {
    let filtrados = concursos;

    // Filtro por busca
    if (busca) {
      filtrados = filtrados.filter(concurso =>
        concurso.titulo.toLowerCase().includes(busca.toLowerCase()) ||
        concurso.orgao.toLowerCase().includes(busca.toLowerCase()) ||
        concurso.banca.toLowerCase().includes(busca.toLowerCase())
      );
    }

    // Filtros específicos
    if (filtros.banca) {
      filtrados = filtrados.filter(concurso =>
        concurso.banca.toLowerCase().includes(filtros.banca.toLowerCase())
      );
    }

    if (filtros.orgao) {
      filtrados = filtrados.filter(concurso =>
        concurso.orgao.toLowerCase().includes(filtros.orgao.toLowerCase())
      );
    }

    if (filtros.nivel) {
      filtrados = filtrados.filter(concurso =>
        concurso.nivel === filtros.nivel
      );
    }

    if (filtros.status) {
      filtrados = filtrados.filter(concurso =>
        concurso.status === filtros.status
      );
    }

    setConcursosFiltrados(filtrados);
  };

  const analisarConcurso = async (concursoId: string) => {
    try {
      setAnalisando(concursoId);
      
      // Buscar conteúdo do edital
      const response = await fetch(`${API_BASE_URL}/editais/concursos/${concursoId}/edital`);
      
      if (!response.ok) {
        throw new Error('Erro ao buscar edital');
      }
      
      const data = await response.json();
      
      // Redirecionar para página de análise com os dados
      const params = new URLSearchParams({
        concurso_id: concursoId,
        titulo: data.titulo,
        conteudo: data.conteudo,
        url_edital: data.url_edital,
        fonte: data.fonte
      });
      
      window.location.href = `/analise-editais?${params.toString()}`;
      
    } catch (error) {
      console.error('Erro ao analisar concurso:', error);
      alert('Erro ao analisar concurso. Tente novamente.');
    } finally {
      setAnalisando(null);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'inscricoes_abertas':
        return 'bg-green-100 text-green-800';
      case 'em_andamento':
        return 'bg-blue-100 text-blue-800';
      case 'finalizado':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'inscricoes_abertas':
        return 'Inscrições Abertas';
      case 'em_andamento':
        return 'Em Andamento';
      case 'finalizado':
        return 'Finalizado';
      default:
        return status;
    }
  };

  const getNivelText = (nivel: string) => {
    switch (nivel) {
      case 'superior':
        return 'Superior';
      case 'medio':
        return 'Médio';
      case 'superior_medio':
        return 'Superior/Médio';
      default:
        return nivel;
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center min-h-screen">
          <div className="animate-spin rounded-full border-2 border-gray-300 border-t-primary-600 h-8 w-8"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <Search className="h-8 w-8 text-blue-600" />
          <h1 className="text-3xl font-bold text-gray-900">Selecionar Concurso</h1>
        </div>
        <p className="text-gray-600 text-lg">
          Escolha um concurso público para análise automática do edital
        </p>
      </div>

      {/* Filtros */}
      <Card className="p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Filter className="h-5 w-5" />
          Filtros
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          {/* Busca */}
          <div>
            <Label htmlFor="busca">Buscar</Label>
            <Input
              id="busca"
              placeholder="Título, órgão ou banca..."
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
            />
          </div>

          {/* Banca */}
          <div>
            <Label htmlFor="banca">Banca</Label>
            <Input
              id="banca"
              placeholder="CESPE, FCC, FGV..."
              value={filtros.banca}
              onChange={(e) => setFiltros({...filtros, banca: e.target.value})}
            />
          </div>

          {/* Órgão */}
          <div>
            <Label htmlFor="orgao">Órgão</Label>
            <Input
              id="orgao"
              placeholder="TRT, MPU, TJ..."
              value={filtros.orgao}
              onChange={(e) => setFiltros({...filtros, orgao: e.target.value})}
            />
          </div>

          {/* Nível */}
          <div>
            <Label htmlFor="nivel">Nível</Label>
            <select
              id="nivel"
              className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
              value={filtros.nivel}
              onChange={(e) => setFiltros({...filtros, nivel: e.target.value})}
            >
              <option value="">Todos</option>
              <option value="superior">Superior</option>
              <option value="medio">Médio</option>
              <option value="superior_medio">Superior/Médio</option>
            </select>
          </div>

          {/* Status */}
          <div>
            <Label htmlFor="status">Status</Label>
            <select
              id="status"
              className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
              value={filtros.status}
              onChange={(e) => setFiltros({...filtros, status: e.target.value})}
            >
              <option value="">Todos</option>
              <option value="inscricoes_abertas">Inscrições Abertas</option>
              <option value="em_andamento">Em Andamento</option>
              <option value="finalizado">Finalizado</option>
            </select>
          </div>
        </div>
      </Card>

      {/* Resultados */}
      <div className="mb-4">
        <p className="text-gray-600">
          {concursosFiltrados.length} concurso(s) encontrado(s)
        </p>
      </div>

      {/* Lista de Concursos */}
      <div className="space-y-6">
        {concursosFiltrados.map((concurso) => (
          <Card key={concurso.id} className="p-6">
            <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4">
              {/* Informações do Concurso */}
              <div className="flex-1">
                <div className="flex items-start justify-between mb-3">
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    {concurso.titulo}
                  </h3>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(concurso.status)}`}>
                    {getStatusText(concurso.status)}
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
                  <div className="flex items-center gap-2">
                    <Users className="h-4 w-4 text-gray-500" />
                    <span className="text-sm text-gray-600">
                      <strong>{concurso.vagas}</strong> vagas
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <DollarSign className="h-4 w-4 text-gray-500" />
                    <span className="text-sm text-gray-600">
                      {concurso.salario}
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <GraduationCap className="h-4 w-4 text-gray-500" />
                    <span className="text-sm text-gray-600">
                      {getNivelText(concurso.nivel)}
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <Calendar className="h-4 w-4 text-gray-500" />
                    <span className="text-sm text-gray-600">
                      Inscrições: {concurso.inscricoes}
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <Clock className="h-4 w-4 text-gray-500" />
                    <span className="text-sm text-gray-600">
                      Prova: {concurso.prova}
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <FileText className="h-4 w-4 text-gray-500" />
                    <span className="text-sm text-gray-600">
                      {concurso.banca}
                    </span>
                  </div>
                </div>

                <div className="mb-4">
                  <p className="text-sm text-gray-600 mb-2">
                    <strong>Órgão:</strong> {concurso.orgao}
                  </p>
                  <p className="text-sm text-gray-600 mb-2">
                    <strong>Cargos:</strong> {concurso.cargos.join(', ')}
                  </p>
                  <p className="text-sm text-gray-600">
                    <strong>Fonte:</strong> {concurso.fonte_nome}
                  </p>
                </div>
              </div>

              {/* Ações */}
              <div className="flex flex-col gap-3 lg:min-w-[200px]">
                <Button
                  onClick={() => analisarConcurso(concurso.id)}
                  disabled={analisando === concurso.id}
                  className="w-full"
                >
                  {analisando === concurso.id ? (
                    <>
                      <div className="animate-spin rounded-full border-2 border-white border-t-transparent h-4 w-4 mr-2"></div>
                      Analisando...
                    </>
                  ) : (
                    <>
                      <Brain className="h-4 w-4 mr-2" />
                      Analisar Edital
                    </>
                  )}
                </Button>

                <Button
                  variant="outline"
                  onClick={() => window.open(concurso.edital_url, '_blank')}
                  className="w-full"
                >
                  <ExternalLink className="h-4 w-4 mr-2" />
                  Ver Edital
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {concursosFiltrados.length === 0 && !loading && (
        <Card className="p-8 text-center">
          <Search className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Nenhum concurso encontrado
          </h3>
          <p className="text-gray-600">
            Tente ajustar os filtros ou buscar por outros termos.
          </p>
        </Card>
      )}
    </div>
  );
}
