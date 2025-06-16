import os

def fix_windows_optimizer():
    """Corrige o arquivo windows_optimizer.py adicionando a função run() faltante"""
    
    print("🔧 CORRETOR AUTOMÁTICO - WINDOWS OPTIMIZER")
    print("=" * 50)
    
    # Verificar se o arquivo existe
    if not os.path.exists("windows_optimizer.py"):
        print("❌ Arquivo windows_optimizer.py não encontrado!")
        return False
    
    # Ler arquivo atual
    print("📖 Lendo arquivo atual...")
    with open("windows_optimizer.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Verificar se já tem a função run
    if "def run(self):" in content:
        print("✅ Função run() já existe!")
        return True
    
    # Adicionar função run() antes do if __name__ == "__main__":
    run_function = '''
    def run(self):
        """Função principal que executa o loop do otimizador"""
        self.logger.info("Método run() iniciado")
        
        try:
            while True:
                self.logger.debug("Exibindo menu...")
                self.show_menu()
                
                try:
                    choice = input("Escolha uma opção (1-13): ").strip()
                    self.logger.info(f"Usuário escolheu opção: {choice}")
                    
                    if choice == '1':
                        self.logger.info("Executando limpeza avançada...")
                        self.advanced_file_cleanup()
                    elif choice == '2':
                        self.logger.info("Executando otimização de inicialização...")
                        self.startup_optimization()
                    elif choice == '3':
                        self.logger.info("Executando gerenciamento de recursos...")
                        self.system_resources_management()
                    elif choice == '4':
                        self.logger.info("Executando otimização de rede...")
                        self.network_optimization()
                    elif choice == '5':
                        self.logger.info("Executando gerenciamento de hardware...")
                        self.hardware_driver_management()
                    elif choice == '6':
                        self.logger.info("Executando tweaks de registro...")
                        self.advanced_registry_tweaks()
                    elif choice == '7':
                        self.logger.info("Executando ferramentas nativas...")
                        self.native_windows_tools()
                    elif choice == '8':
                        self.logger.info("Executando segurança e performance...")
                        self.security_performance()
                    elif choice == '9':
                        self.logger.info("Executando otimizações específicas...")
                        self.specific_case_optimization()
                    elif choice == '10':
                        self.logger.info("Executando dicas diversas...")
                        self.miscellaneous_tips()
                    elif choice == '11':
                        self.logger.info("Exibindo informações do sistema...")
                        self.show_detailed_system_info()
                    elif choice == '12':
                        self.logger.info("Executando otimização completa...")
                        self.complete_optimization()
                    elif choice == '13':
                        self.logger.info("Usuário escolheu sair...")
                        print("👋 Saindo do otimizador...")
                        sys.exit(0)
                    else:
                        self.logger.warning(f"Opção inválida escolhida: {choice}")
                        print("❌ Opção inválida!")
                        
                    input("\\nPressione Enter para continuar...")
                    
                except Exception as e:
                    self.logger.error(f"Erro no loop principal: {e}")
                    self.logger.error(traceback.format_exc())
                    print(f"❌ Erro: {str(e)}")
                    input("\\nPressione Enter para continuar...")
                    
        except KeyboardInterrupt:
            self.logger.info("Programa interrompido pelo usuário (Ctrl+C)")
            print("\\n👋 Saindo do otimizador...")
            sys.exit(0)
        except Exception as e:
            self.logger.error(f"Erro fatal no método run(): {e}")
            self.logger.error(traceback.format_exc())
            raise

'''
    
    # Inserir função antes do if __name__
    if 'if __name__ == "__main__":' in content:
        # Dividir conteúdo
        parts = content.split('if __name__ == "__main__":')
        
        # Adicionar função run antes do main
        new_content = parts[0] + run_function + '\nif __name__ == "__main__":' + parts[1]
        
        # Criar backup
        print("💾 Criando backup...")
        with open("windows_optimizer_backup.py", "w", encoding="utf-8") as f:
            f.write(content)
        
        # Salvar arquivo corrigido
        print("💾 Salvando arquivo corrigido...")
        with open("windows_optimizer.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        
        print("✅ Arquivo corrigido com sucesso!")
        print("📄 Backup salvo como: windows_optimizer_backup.py")
        return True
    else:
        print("❌ Não foi possível encontrar local para inserir função")
        return False

def main():
    print("🔧 CORRETOR AUTOMÁTICO")
    print("🎯 Este script corrige o Windows Optimizer automaticamente")
    print()
    
    try:
        if fix_windows_optimizer():
            print("\n🎉 CORREÇÃO CONCLUÍDA!")
            print("✅ O Windows Optimizer agora deve funcionar")
            print("🚀 Execute: python windows_optimizer.py")
        else:
            print("\n💥 FALHA NA CORREÇÃO")
            print("❌ Verifique o arquivo manualmente")
    
    except Exception as e:
        print(f"\n💥 ERRO: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()
