# Windows Performance Optimizer v2.0

Ferramenta avançada de linha de comando para otimização completa do Windows.

## 🚀 Novos Recursos v2.0

### 🧹 Limpeza Avançada
- **Arquivos Temporários**: Remove arquivos de %Temp%, Windows\Temp, cache de atualizações
- **Cache de Navegadores**: Chrome, Edge, Firefox, Opera
- **Logs do Sistema**: Windows\Logs, CBS logs, relatórios de erro
- **Arquivos de Hibernação**: Desativa hibernação para liberar espaço
- **Prefetch**: Limpa arquivos de inicialização
- **Thumbnails**: Remove cache de miniaturas

### 🚫 Serviços Desnecessários
- Xbox Live e Gaming
- Fax e Telefonia
- Smart Card
- Geolocalização
- Relatórios de Erro
- Telemetria do Windows
- BitLocker (se não usado)

### ⚡ Otimizações de Performance
- Efeitos visuais otimizados
- Plano de energia alto desempenho
- TRIM habilitado para SSDs
- Memória virtual otimizada
- Menu de contexto mais rápido

### 🔧 Registro Avançado
- Desabilita paginação executiva
- Otimiza cache do sistema
- Remove delays de interface
- Desabilita telemetria
- Desabilita Cortana

### 📱 Remoção de Bloatware
- Apps da Microsoft Store desnecessários
- Jogos pré-instalados (Candy Crush, etc.)
- Xbox Apps (se não usado)
- Office Hub
- 3D Viewer e Print 3D

### 🔄 Manutenção Automática
- Verificação de integridade (SFC)
- Reparo de imagem do sistema (DISM)
- Verificação de erros de disco
- Desfragmentação inteligente (apenas HDD)

### 💻 Informações Detalhadas
- Uso de CPU e memória em tempo real
- Informações de disco
- Top processos por CPU/memória
- Detecção automática SSD/HDD

## 📋 Como Usar

### Opções do Menu:
1. **Limpeza Temporários**: Remove arquivos temp, cache, logs
2. **Cache Avançado**: Limpa navegadores, DNS, lixeira
3. **Desativar Serviços**: Para serviços desnecessários
4. **Otimizar Performance**: Configura sistema para velocidade
5. **Registro Avançado**: Aplica tweaks do registro
6. **Remover Bloatware**: Remove apps pré-instalados
7. **Manutenção**: SFC, DISM, ChkDsk, desfrag
8. **Info Sistema**: Mostra uso detalhado de recursos
9. **Otimização Completa**: Executa TODAS as opções
10. **Sair**: Fecha o programa

## ⚠️ Avisos Importantes

- **Execute como ADMINISTRADOR** para máxima efetividade
- **Faça backup** antes de usar otimizações de registro
- **Reinicie o PC** após otimização completa
- Algumas mudanças são permanentes
- Testado no Windows 10/11

## 🛠️ Instalação

### Método 1: Python
```bash
pip install -r requirements.txt
python windows_optimizer.py
```

### Método 2: Executável
```bash
python build_exe.py
dist/WindowsOptimizer.exe
```

## 📊 Resultados Esperados

- ⬆️ **Velocidade de inicialização** mais rápida
- ⬆️ **Responsividade** do sistema melhorada
- ⬇️ **Uso de RAM** reduzido
- ⬇️ **Uso de disco** otimizado
- ⬇️ **Processos em background** minimizados
- 🔋 **Vida útil da bateria** melhorada (laptops)

## 🔧 Requisitos Técnicos

- Windows 10 versão 1903+ ou Windows 11
- Python 3.7+ (para desenvolvimento)
- Privilégios de administrador
- 50MB espaço livre em disco

## 📝 Changelog v2.0

- ✅ Interface melhorada com emojis
- ✅ 40+ novas otimizações implementadas
- ✅ Detecção automática de SSD/HDD
- ✅ Remoção inteligente de bloatware
- ✅ Monitoramento de recursos em tempo real
- ✅ Logs detalhados de operações
- ✅ Verificação de privilégios administrativos

## 🤝 Suporte

Para reportar bugs ou sugerir melhorias, abra uma issue no repositório.
