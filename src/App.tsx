import { useState } from 'react';
import { Button } from './components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './components/ui/table';
import { FileUp, Play, Bug, CheckCircle, Refresh, AlertCircle, Loader2 } from 'lucide-react';
import { Textarea } from './components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from './components/ui/dialog';
import { Alert, AlertDescription } from './components/ui/alert';

const API_URL = 'http://localhost:5000/api';

interface Token {
  type: string;
  lexeme: string;
  line: number;
  column: number;
}

interface Error {
  line: number;
  column: number;
  message: string;
}

interface Symbol {
  scope: string;
  name: string;
  type: string;
  status: string;
}

export default function App() {
  const [tokens, setTokens] = useState<Token[]>([]);
  const [errors, setErrors] = useState<Error[]>([]);
  const [symbols, setSymbols] = useState<Symbol[]>([]);
  const [ast, setAst] = useState<string>('');
  const [code, setCode] = useState<string>('// Ingrese su código C# aquí\nint x = 10;\nConsole.WriteLine(x);');
  const [isCodeDialogOpen, setIsCodeDialogOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [analysisMessage, setAnalysisMessage] = useState<string>('');
  const [analysisType, setAnalysisType] = useState<'success' | 'error' | ''>('');

  const handleLoadCode = () => {
    setIsCodeDialogOpen(true);
  };

  const showMessage = (message: string, type: 'success' | 'error') => {
    setAnalysisMessage(message);
    setAnalysisType(type);
    setTimeout(() => {
      setAnalysisMessage('');
      setAnalysisType('');
    }, 5000);
  };

  const handleAnalyzeLexical = async () => {
    if (!code.trim()) {
      showMessage('Por favor ingrese código para analizar', 'error');
      return;
    }

    setLoading(true);
    // Limpiar resultados anteriores
    setTokens([]);
    setErrors([]);
    setAst('');
    setSymbols([]);
    
    try {
      const response = await fetch(`${API_URL}/analyze/lexical`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
      });

      const data = await response.json();
      
      if (data.success) {
        setTokens(data.tokens);
        setErrors(data.errors || []);
        showMessage(data.message, 'success');
      } else {
        showMessage(data.message || 'Error en análisis léxico', 'error');
      }
    } catch (error) {
      showMessage('Error de conexión con el servidor. ¿Está ejecutando el backend?', 'error');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeSyntax = async () => {
    if (!code.trim()) {
      showMessage('Por favor ingrese código para analizar', 'error');
      return;
    }

    setLoading(true);
    // Limpiar resultados anteriores
    setTokens([]);
    setErrors([]);
    setAst('');
    setSymbols([]);
    
    try {
      // Primero hacer análisis léxico
      const lexicalResponse = await fetch(`${API_URL}/analyze/lexical`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
      });
      const lexicalData = await lexicalResponse.json();
      if (lexicalData.success) {
        setTokens(lexicalData.tokens);
      }

      // Luego análisis sintáctico
      const response = await fetch(`${API_URL}/analyze/syntactic`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
      });

      const data = await response.json();
      
      if (data.success) {
        setAst(data.ast);
        setErrors(data.errors || []);
        showMessage(data.message, 'success');
      } else {
        setErrors(data.errors || []);
        showMessage(data.message || 'Error en análisis sintáctico', 'error');
      }
    } catch (error) {
      showMessage('Error de conexión con el servidor. ¿Está ejecutando el backend?', 'error');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeSemantic = async () => {
    if (!code.trim()) {
      showMessage('Por favor ingrese código para analizar', 'error');
      return;
    }

    setLoading(true);
    // Limpiar resultados anteriores
    setTokens([]);
    setErrors([]);
    setAst('');
    setSymbols([]);
    
    try {
      // Primero hacer análisis léxico
      const lexicalResponse = await fetch(`${API_URL}/analyze/lexical`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
      });
      const lexicalData = await lexicalResponse.json();
      if (lexicalData.success) {
        setTokens(lexicalData.tokens);
      }

      // Luego análisis sintáctico
      const syntacticResponse = await fetch(`${API_URL}/analyze/syntactic`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
      });
      const syntacticData = await syntacticResponse.json();
      if (syntacticData.success) {
        setAst(syntacticData.ast);
      }

      // Finalmente análisis semántico
      const response = await fetch(`${API_URL}/analyze/semantic`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
      });

      const data = await response.json();
      
      if (data.success) {
        setErrors(data.errors || []);
        setSymbols(data.symbols || []);
        showMessage(data.message, 'success');
      } else {
        setErrors(data.errors || []);
        setSymbols(data.symbols || []);
        showMessage(data.message || 'Error en análisis semántico', 'error');
      }
    } catch (error) {
      showMessage('Error de conexión con el servidor. ¿Está ejecutando el backend?', 'error');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeAll = async () => {
    if (!code.trim()) {
      showMessage('Por favor ingrese código para analizar', 'error');
      return;
    }

    setLoading(true);
    // Limpiar resultados anteriores
    setTokens([]);
    setErrors([]);
    setAst('');
    setSymbols([]);
    
    try {
      const response = await fetch(`${API_URL}/analyze/all`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
      });

      const data = await response.json();
      
      if (data.success && data.result) {
        // Actualizar todos los estados con los resultados
        setTokens(data.result.lexical.tokens || []);
        setAst(data.result.syntactic.ast || '');
        setSymbols(data.result.symbols || []);
        
        // Combinar todos los errores
        const allErrors = [
          ...(data.result.lexical.errors || []),
          ...(data.result.syntactic.errors || []),
          ...(data.result.semantic.errors || [])
        ];
        setErrors(allErrors);
        
        showMessage(data.message, 'success');
      } else {
        const allErrors = data.result ? [
          ...(data.result.lexical?.errors || []),
          ...(data.result.syntactic?.errors || []),
          ...(data.result.semantic?.errors || [])
        ] : [];
        setErrors(allErrors);
        showMessage(data.message || 'Error en análisis completo', 'error');
      }
    } catch (error) {
      showMessage('Error de conexión con el servidor. ¿Está ejecutando el backend?', 'error');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-white">
      {/* Header / Barra superior */}
      <header className="bg-[#E9E9E9] px-6 py-3 border-b border-gray-300">
        {/* Mensaje de análisis */}
        {analysisMessage && (
          <Alert className={`mb-3 ${analysisType === 'success' ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
            {analysisType === 'success' ? (
              <CheckCircle className="h-4 w-4 text-green-600" />
            ) : (
              <AlertCircle className="h-4 w-4 text-red-600" />
            )}
            <AlertDescription className={analysisType === 'success' ? 'text-green-800' : 'text-red-800'}>
              {analysisMessage}
            </AlertDescription>
          </Alert>
        )}
        
        <div className="flex items-center gap-4">
          <Dialog open={isCodeDialogOpen} onOpenChange={setIsCodeDialogOpen}>
            <DialogTrigger asChild>
              <Button 
                onClick={handleLoadCode}
                className="bg-blue-600 hover:bg-blue-700 text-white"
              >
                <FileUp className="mr-2 h-4 w-4" />
                Cargar Código
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-2xl">
              <DialogHeader>
                <DialogTitle>Cargar Código C#</DialogTitle>
              </DialogHeader>
              <Textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="Ingrese su código C# aquí..."
                className="min-h-[300px] font-mono"
              />
              <Button onClick={() => setIsCodeDialogOpen(false)}>
                Guardar
              </Button>
            </DialogContent>
          </Dialog>

          <Button 
            onClick={handleAnalyzeLexical}
            variant="outline"
            className="bg-white hover:bg-gray-100"
            disabled={loading}
          >
            {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Play className="mr-2 h-4 w-4" />}
            Analizar Léxico
          </Button>

          <Button 
            onClick={handleAnalyzeSyntax}
            variant="outline"
            className="bg-white hover:bg-gray-100"
            disabled={loading}
          >
            {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Play className="mr-2 h-4 w-4" />}
            Analizar Sintaxis
          </Button>

          <Button 
            onClick={handleAnalyzeSemantic}
            variant="outline"
            className="bg-white hover:bg-gray-100"
            disabled={loading}
          >
            {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Bug className="mr-2 h-4 w-4" />}
            Analizar Semántica
          </Button>

          <Button 
            onClick={handleAnalyzeAll}
            className="bg-green-600 hover:bg-green-700 text-white"
            disabled={loading}
          >
            {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <CheckCircle className="mr-2 h-4 w-4" />}
            Analizar Todo
          </Button>
        </div>
      </header>

      {/* Panel central con pestañas */}
      <main className="flex-1 p-6">
        <Tabs defaultValue="tokens" className="w-full">
          <TabsList className="bg-[#F8F8F8] w-full justify-start border-b border-gray-200 rounded-none h-auto p-0">
            <TabsTrigger 
              value="tokens"
              className="data-[state=active]:bg-white data-[state=active]:border-b-2 data-[state=active]:border-blue-600 rounded-none px-6 py-3"
            >
              🧩 Tokens
            </TabsTrigger>
            <TabsTrigger 
              value="errors"
              className="data-[state=active]:bg-white data-[state=active]:border-b-2 data-[state=active]:border-blue-600 rounded-none px-6 py-3"
            >
              🧠 Errores
            </TabsTrigger>
            <TabsTrigger 
              value="symbols"
              className="data-[state=active]:bg-white data-[state=active]:border-b-2 data-[state=active]:border-blue-600 rounded-none px-6 py-3"
            >
              🗂 Tabla de Símbolos
            </TabsTrigger>
            <TabsTrigger 
              value="ast"
              className="data-[state=active]:bg-white data-[state=active]:border-b-2 data-[state=active]:border-blue-600 rounded-none px-6 py-3"
            >
              🌳 Árbol Sintáctico (AST)
            </TabsTrigger>
          </TabsList>

          {/* Contenido de Tokens */}
          <TabsContent value="tokens" className="mt-6">
            <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Tipo</TableHead>
                    <TableHead>Lexema</TableHead>
                    <TableHead>Línea</TableHead>
                    <TableHead>Columna</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {tokens.map((token, index) => (
                    <TableRow key={index}>
                      <TableCell className="text-blue-600">{token.type}</TableCell>
                      <TableCell className="font-mono">{token.lexeme}</TableCell>
                      <TableCell>{token.line}</TableCell>
                      <TableCell>{token.column}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </TabsContent>

          {/* Contenido de Errores */}
          <TabsContent value="errors" className="mt-6">
            <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
              {errors.length > 0 ? (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Línea</TableHead>
                      <TableHead>Columna</TableHead>
                      <TableHead>Mensaje</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {errors.map((error, index) => (
                      <TableRow key={index}>
                        <TableCell>{error.line}</TableCell>
                        <TableCell>{error.column}</TableCell>
                        <TableCell className="text-red-600">{error.message}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              ) : (
                <div className="text-center py-12 text-gray-500">
                  <CheckCircle className="h-12 w-12 mx-auto mb-4 text-green-500" />
                  <p>No se encontraron errores</p>
                </div>
              )}
            </div>
          </TabsContent>

          {/* Contenido de Tabla de Símbolos */}
          <TabsContent value="symbols" className="mt-6">
            <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Ámbito</TableHead>
                    <TableHead>Nombre</TableHead>
                    <TableHead>Tipo</TableHead>
                    <TableHead>Estado</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {symbols.map((symbol, index) => (
                    <TableRow key={index}>
                      <TableCell className="text-purple-600">{symbol.scope}</TableCell>
                      <TableCell className="font-mono">{symbol.name}</TableCell>
                      <TableCell className="text-blue-600">{symbol.type}</TableCell>
                      <TableCell>
                        <span className={symbol.status === 'Asignado' ? 'text-green-600' : 'text-gray-600'}>
                          {symbol.status}
                        </span>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </TabsContent>

          {/* Contenido de Árbol Sintáctico */}
          <TabsContent value="ast" className="mt-6">
            <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
              <div className="bg-gray-50 rounded-lg p-6 border border-gray-200">
                <pre className="font-mono text-gray-800 whitespace-pre-wrap">
                  {ast}
                </pre>
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </main>

      {/* Footer */}
      <footer className="bg-[#F0F0F0] py-3 border-t border-gray-300">
        <p className="text-center text-[#666]">
          Desarrollado por Daniel Vilema, Kiara Morán y Juan Romero — 2025
        </p>
      </footer>
    </div>
  );
}
