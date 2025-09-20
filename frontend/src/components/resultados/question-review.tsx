import { Card } from '@/components/ui/card'

export function QuestionReview() {
  return (
    <Card className="p-6">
      <h3 className="text-lg font-semibold mb-4">
        Revisão das Questões
      </h3>
      <div className="space-y-4">
        <div className="border-l-4 border-red-500 pl-4">
          <p className="font-medium mb-2">
            Questão 1 - Errada ❌
          </p>
          <p className="text-sm text-gray-600 mb-2">
            Qual é a capital do Brasil?
          </p>
          <p className="text-sm">
            <span className="font-medium">Sua resposta:</span> Rio de Janeiro<br/>
            <span className="font-medium">Resposta correta:</span> Brasília
          </p>
        </div>
        
        <div className="border-l-4 border-green-500 pl-4">
          <p className="font-medium mb-2">
            Questão 2 - Correta ✅
          </p>
          <p className="text-sm text-gray-600 mb-2">
            Quem escreveu &quot;Os Lusíadas&quot;?
          </p>
          <p className="text-sm">
            <span className="font-medium">Sua resposta:</span> Luís de Camões ✅
          </p>
        </div>
      </div>
    </Card>
  )
}
