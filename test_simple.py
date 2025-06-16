import sys
import os

def test_basic_functionality():
    """Teste muito básico para verificar se o otimizador funciona"""
    print("🔍 TESTE BÁSICO DO WINDOWS OPTIMIZER")
    print("=" * 50)
    
    try:
        # Importar o otimizador
        print("📦 Importando WindowsOptimizer...")
        from windows_optimizer import WindowsOptimizer
        print("✅ WindowsOptimizer importado com sucesso")
        
        # Criar instância
        print("🔧 Criando instância...")
        optimizer = WindowsOptimizer()
        print("✅ WindowsOptimizer instanciado com sucesso")
        
        # Testar função básica
        print("🖥️  Testando função básica...")
        optimizer.clear_screen()
        print("✅ Função clear_screen funcionou")
        
        # Verificar se tem método run
        if hasattr(optimizer, 'run'):
            print("✅ Método run() encontrado")
        else:
            print("❌ Método run() NÃO encontrado")
            return False
        
        # Testar exibição de menu
        print("📋 Testando exibição de menu...")
        optimizer.print_header()
        print("✅ Header exibido com sucesso")
        
        print("\n🎉 TODOS OS TESTES BÁSICOS PASSARAM!")
        print("✅ O otimizador parece estar funcionando corretamente")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        print("\nDETALHES DO ERRO:")
        print(traceback.format_exc())
        return False

def run_limited_test():
    """Executa um teste limitado sem usar o run() completo"""
    try:
        from windows_optimizer import WindowsOptimizer
        
        print("\n🧪 TESTE LIMITADO:")
        optimizer = WindowsOptimizer()
        
        # Testar informações do sistema
        print("💻 Testando informações do sistema...")
        optimizer.show_detailed_system_info()
        
        print("\n✅ Teste limitado concluído!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste limitado: {e}")
        return False

def main():
    print("🚀 TESTE SIMPLES - WINDOWS OPTIMIZER")
    print("🎯 Verificando funcionalidade básica\n")
    
    # Teste básico
    if not test_basic_functionality():
        print("\n💥 FALHA NOS TESTES BÁSICOS")
        input("Pressione Enter para sair...")
        return
    
    # Perguntar se quer testar funcionalidade
    print("\n" + "="*50)
    choice = input("Deseja testar funcionalidade básica? (s/N): ").lower().strip()
    
    if choice == 's':
        run_limited_test()
    
    print("\n" + "="*50)
    print("🎯 TESTE CONCLUÍDO")
    print("💡 Se chegou até aqui, o otimizador deve funcionar!")
    print("🔧 Para usar: python windows_optimizer.py")
    
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"💥 ERRO CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione Enter para sair...")
