'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
// import { Badge } from '@/components/ui/badge';
import { 
  FileText, 
  Upload, 
  Brain, 
  Calendar, 
  DollarSign, 
  Users, 
  BookOpen,
  Clock,
  CheckCircle,
  AlertCircle,
  Loader2,
  Search
} from 'lucide-react';

interface EditalAnalysis {
  status: string;
  resultado: {
    metadados: {
      data_analise: string;
      tamanho_texto: number;
      palavras_totais: number;
      versao_analisador: string;
      status: string;
    };
    analise_basica: {
      tipo_documento: string;
      banca_organizadora: string;
      orgao_responsavel: string;
      numero_secoes: number;
      numero_paragrafos: number;
      palavras_totais: number;
    };
    informacoes_extraidas: {
      cargos: Array<{ cargo: string; contexto: string }>;
      vagas: Array<{ numero_vagas: number; contexto: string }>;
      disciplinas: Array<{ disciplina: string; tipo: string; contexto: string }>;
      datas: Array<{ data: string; tipo: string; contexto: string }>;
      valores: Array<{ valor: number; valor_formatado: string; tipo: string; contexto: string }>;
      etapas: Array<{ etapa: string; tipo: string }>;
    };
    resumo_executivo: string;
    analise_relevancia: {
      score_relevancia: number;
      relevancia_percentual: number;
      classificacao: string;
    };
  };
  tempo_processamento: number;
}

export default function AnaliseEditaisPage() {
  const searchParams = useSearchParams();
  const [conteudoEdital, setConteudoEdital] = useState('');
  const [urlEdital, setUrlEdital] = useState('');
  const [banca, setBanca] = useState('');
  const [loading, setLoading] = useState(false);
  const [resultado, setResultado] = useState<EditalAnalysis | null>(null);
  const [erro, setErro] = useState('');
  const [concursoSelecionado, setConcursoSelecionado] = useState<any>(null);

  const API_BASE_URL = 'http://localhost:8002';

  // Carregar dados do concurso selecionado
  useEffect(() => {
    if (!searchParams) return;
    
    const concursoId = searchParams.get('concurso_id');
    const titulo = searchParams.get('titulo');
    const conteudo = searchParams.get('conteudo');
    const url = searchParams.get('url_edital');
    const fonte = searchParams.get('fonte');

    if (concursoId && titulo && conteudo) {
      setConcursoSelecionado({
        id: concursoId,
        titulo: titulo,
        conteudo: conteudo,
        url_edital: url,
        fonte: fonte
      });
      
      setConteudoEdital(conteudo);
      if (url) setUrlEdital(url);
      if (fonte) setBanca(fonte);
    }
  }, [searchParams]);

  const analisarEdital = async () => {
    if (!conteudoEdital.trim()) {
      setErro('Por favor, insira o conteúdo do edital para análise.');
      return;
    }

    if (conteudoEdital.length < 100) {
      setErro('O conteúdo do edital deve ter pelo menos 100 caracteres.');
      return;
    }

    setLoading(true);
    setErro('');
    setResultado(null);

    try {
      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          conteudo: conteudoEdital,
          url_edital: urlEdital || null,
          banca: banca || null
        })
      });

      const data = await response.json();

      if (response.ok) {
        setResultado(data);
      } else {
        throw new Error(data.detail || 'Erro na análise');
      }

    } catch (error) {
      console.error('Erro:', error);
      setErro(`Erro na análise: ${error instanceof Error ? error.message : 'Erro desconhecido'}`);
    } finally {
      setLoading(false);
    }
  };

  const carregarExemplo = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/analyze/sample`);
      const data = await response.json();
      
      if (response.ok) {
        const editalExemplo = `
EDITAL Nº 1 – DGP/DPF, DE 15 DE JUNHO DE 2023
CONCURSO PÚBLICO PARA O PROVIMENTO DE VAGAS NO CARGO DE AGENTE DE POLÍCIA FEDERAL

O DIRETOR-GERAL DA POLÍCIA FEDERAL, no uso de suas atribuições, torna pública a realização de concurso público para o provimento de 1.500 vagas no cargo de Agente de Polícia Federal.

1 DAS DISPOSIÇÕES PRELIMINARES
1.1 O concurso público será regido por este edital e executado pelo Centro Brasileiro de Pesquisa em Avaliação e Seleção e de Promoção de Eventos (Cebraspe).
1.2 O cargo de Agente de Polícia Federal exige nível superior em qualquer área de formação.
1.3 A remuneração inicial é de R$ 12.522,50.

2 DAS INSCRIÇÕES
2.1 As inscrições poderão ser realizadas no período de 20/07/2023 a 02/08/2023.
2.2 A taxa de inscrição é de R$ 180,00.

3 DAS ETAPAS DO CONCURSO
3.1 Prova Objetiva e Discursiva: 19/09/2023.
3.2 Exame de Aptidão Física.
3.3 Avaliação Médica.
3.4 Avaliação Psicológica.

4 DAS DISCIPLINAS
Serão cobradas as seguintes disciplinas: Língua Portuguesa, Noções de Direito Administrativo, Noções de Direito Constitucional, Raciocínio Lógico, Informática, Contabilidade Geral.
        `;
        
        setConteudoEdital(editalExemplo.trim());
        setBanca('CESPE/CEBRASPE');
        setUrlEdital('https://exemplo.com/edital-pf');
        setErro('');
      } else {
        throw new Error('Erro ao carregar exemplo');
      }
    } catch (error) {
      console.error('Erro:', error);
      setErro('Erro ao carregar edital de exemplo. Verifique se o servidor está rodando.');
    }
  };

  const limparFormulario = () => {
    setConteudoEdital('');
    setUrlEdital('');
    setBanca('');
    setResultado(null);
    setErro('');
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <Brain className="h-8 w-8 text-blue-600" />
          <h1 className="text-3xl font-bold text-gray-900">Análise de Editais com IA</h1>
        </div>
        <p className="text-gray-600 text-lg">
          Sistema inteligente de análise de editais de concursos públicos
        </p>
        
        {/* Indicador de concurso selecionado */}
        {concursoSelecionado && (
          <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <CheckCircle className="h-5 w-5 text-green-600" />
              <span className="font-semibold text-green-800">Concurso Selecionado</span>
            </div>
            <p className="text-green-700">
              <strong>{concursoSelecionado.titulo}</strong>
            </p>
            <p className="text-sm text-green-600">
              Fonte: {concursoSelecionado.fonte} | 
              <a 
                href={concursoSelecionado.url_edital} 
                target="_blank" 
                rel="noopener noreferrer"
                className="ml-1 underline hover:text-green-800"
              >
                Ver edital original
              </a>
            </p>
          </div>
        )}
      </div>

      {/* Formulário */}
      <Card className="p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <FileText className="h-5 w-5" />
          Análise de Edital
        </h2>

        <div className="space-y-4">
        <div className="flex gap-4">
          <Button
            onClick={carregarExemplo}
            variant="outline"
            className="flex items-center gap-2"
          >
            <Upload className="h-4 w-4" />
            Carregar Exemplo
          </Button>
          <Button
            onClick={limparFormulario}
            variant="outline"
            className="flex items-center gap-2"
          >
            Limpar
          </Button>
          <Button
            onClick={() => window.location.href = '/selecionar-concurso'}
            variant="outline"
            className="flex items-center gap-2"
          >
            <Search className="h-4 w-4" />
            Selecionar Concurso
          </Button>
        </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="urlEdital">URL do Edital (opcional)</Label>
              <Input
                id="urlEdital"
                type="url"
                placeholder="https://exemplo.com/edital.pdf"
                value={urlEdital}
                onChange={(e) => setUrlEdital(e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="banca">Banca Organizadora (opcional)</Label>
              <Input
                id="banca"
                placeholder="CESPE, FGV, FCC, etc."
                value={banca}
                onChange={(e) => setBanca(e.target.value)}
              />
            </div>
          </div>

          <div>
            <Label htmlFor="conteudoEdital">Conteúdo do Edital</Label>
            <Textarea
              id="conteudoEdital"
              placeholder="Cole aqui o conteúdo do edital que deseja analisar..."
              value={conteudoEdital}
              onChange={(e) => setConteudoEdital(e.target.value)}
              rows={8}
              className="mt-1"
            />
          </div>

          <Button 
            onClick={analisarEdital}
            disabled={loading}
            className="w-full md:w-auto"
          >
            {loading ? (
              <>
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                Analisando...
              </>
            ) : (
              <>
                <Brain className="h-4 w-4 mr-2" />
                Analisar Edital
              </>
            )}
          </Button>
        </div>

        {erro && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2">
            <AlertCircle className="h-5 w-5 text-red-600" />
            <span className="text-red-800">{erro}</span>
          </div>
        )}
      </Card>

      {/* Loading */}
      {loading && (
        <Card className="p-6 text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4 text-blue-600" />
          <p className="text-gray-600">Analisando edital com IA...</p>
        </Card>
      )}

      {/* Resultados */}
      {resultado && (
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-gray-900">Resultados da Análise</h2>

          {/* Informações Básicas */}
          <Card className="p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <CheckCircle className="h-5 w-5 text-green-600" />
              Informações Básicas
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div>
                <Label className="text-sm font-medium text-gray-500">Status</Label>
                <p className="text-green-600 font-semibold">{resultado.status}</p>
              </div>
              <div>
                <Label className="text-sm font-medium text-gray-500">Tempo de Processamento</Label>
                <p className="flex items-center gap-1">
                  <Clock className="h-4 w-4" />
                  {resultado.tempo_processamento.toFixed(2)}s
                </p>
              </div>
              <div>
                <Label className="text-sm font-medium text-gray-500">Tipo de Documento</Label>
                <p>{resultado.resultado.analise_basica?.tipo_documento || 'N/A'}</p>
              </div>
              <div>
                <Label className="text-sm font-medium text-gray-500">Banca Organizadora</Label>
                <p>{resultado.resultado.analise_basica?.banca_organizadora || 'N/A'}</p>
              </div>
              <div>
                <Label className="text-sm font-medium text-gray-500">Órgão Responsável</Label>
                <p>{resultado.resultado.analise_basica?.orgao_responsavel || 'N/A'}</p>
              </div>
              <div>
                <Label className="text-sm font-medium text-gray-500">Palavras Totais</Label>
                <p>{resultado.resultado.analise_basica?.palavras_totais || 0}</p>
              </div>
            </div>
          </Card>

          {/* Estatísticas */}
          <Card className="p-6">
            <h3 className="text-lg font-semibold mb-4">Estatísticas</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">
                  {resultado.resultado.analise_basica?.numero_secoes || 0}
                </div>
                <div className="text-sm text-gray-500">Seções</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">
                  {resultado.resultado.informacoes_extraidas?.disciplinas?.length || 0}
                </div>
                <div className="text-sm text-gray-500">Disciplinas</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">
                  {resultado.resultado.informacoes_extraidas?.datas?.length || 0}
                </div>
                <div className="text-sm text-gray-500">Datas</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-orange-600">
                  {resultado.resultado.informacoes_extraidas?.valores?.length || 0}
                </div>
                <div className="text-sm text-gray-500">Valores</div>
              </div>
            </div>
          </Card>

          {/* Cargos */}
          {resultado.resultado.informacoes_extraidas?.cargos && resultado.resultado.informacoes_extraidas.cargos.length > 0 && (
            <Card className="p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Users className="h-5 w-5" />
                Cargos Identificados
              </h3>
              <div className="space-y-2">
                {resultado.resultado.informacoes_extraidas.cargos.map((cargo, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <span className="font-medium">{cargo.cargo}</span>
                    <span className="px-2 py-1 bg-gray-100 rounded text-sm">{cargo.contexto}</span>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Vagas */}
          {resultado.resultado.informacoes_extraidas?.vagas && resultado.resultado.informacoes_extraidas.vagas.length > 0 && (
            <Card className="p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Users className="h-5 w-5" />
                Vagas
              </h3>
              <div className="space-y-2">
                {resultado.resultado.informacoes_extraidas.vagas.map((vaga, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <span className="font-medium">Número de Vagas</span>
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm font-semibold">{vaga.numero_vagas}</span>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Disciplinas */}
          {resultado.resultado.informacoes_extraidas?.disciplinas && resultado.resultado.informacoes_extraidas.disciplinas.length > 0 && (
            <Card className="p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <BookOpen className="h-5 w-5" />
                Disciplinas
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {resultado.resultado.informacoes_extraidas.disciplinas.map((disciplina, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <span className="font-medium">{disciplina.disciplina}</span>
                    <span className="px-2 py-1 border border-gray-300 rounded text-sm">{disciplina.tipo}</span>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Datas */}
          {resultado.resultado.informacoes_extraidas?.datas && resultado.resultado.informacoes_extraidas.datas.length > 0 && (
            <Card className="p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Calendar className="h-5 w-5" />
                Datas Importantes
              </h3>
              <div className="space-y-2">
                {resultado.resultado.informacoes_extraidas.datas.map((data, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <span className="font-medium">{data.tipo}</span>
                    <span className="px-2 py-1 bg-gray-100 rounded text-sm">{data.data}</span>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Valores */}
          {resultado.resultado.informacoes_extraidas?.valores && resultado.resultado.informacoes_extraidas.valores.length > 0 && (
            <Card className="p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <DollarSign className="h-5 w-5" />
                Valores Monetários
              </h3>
              <div className="space-y-2">
                {resultado.resultado.informacoes_extraidas.valores.map((valor, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <span className="font-medium">{valor.tipo}</span>
                    <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-sm font-semibold">{valor.valor_formatado}</span>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Resumo Executivo */}
          {resultado.resultado.resumo_executivo && (
            <Card className="p-6">
              <h3 className="text-lg font-semibold mb-4">Resumo Executivo</h3>
              <p className="text-gray-700 leading-relaxed">{resultado.resultado.resumo_executivo}</p>
            </Card>
          )}

          {/* Análise de Relevância */}
          {resultado.resultado.analise_relevancia && (
            <Card className="p-6">
              <h3 className="text-lg font-semibold mb-4">Análise de Relevância</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label className="text-sm font-medium text-gray-500">Score</Label>
                  <p className="text-2xl font-bold text-blue-600">
                    {resultado.resultado.analise_relevancia.score_relevancia}
                  </p>
                </div>
                <div>
                  <Label className="text-sm font-medium text-gray-500">Classificação</Label>
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded text-lg font-semibold">
                    {resultado.resultado.analise_relevancia.classificacao}
                  </span>
                </div>
              </div>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
