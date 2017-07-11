import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os

INICIO = 'inicio'
INSUMO = 'insumo'
IMOVEL = 'imovel'
COMPRA_INSUMO = 'compra_insumo'
RELATORIOS = 'relatorios'

class interface:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("interface.glade")
        self.builder.connect_signals(self)

        #janela principal
        self.window = self.builder.get_object("window2")
        self.window.show_all()
        self.janela = INICIO

        #Objetos
        self.janela_inicio = self.builder.get_object("window2")
        self.janela_operacao = self.builder.get_object("window3")
        #Cadastro insumo
        self.janela_cadastro_insumo = self.builder.get_object("window1")
        self.entry_codigo_insumo = self.builder.get_object("entry1")
        self.entry_descricao_insumo = self.builder.get_object("entry2")
        self.entry_unity_insumo = self.builder.get_object("entry3")
        self.btn_save_insumo = self.builder.get_object("button1")
        #cadastro imovel
        self.janela_cadastro_imovel = self.builder.get_object("window4")
        self.entry_endereco_imovel = self.builder.get_object("entry4")
        self.entry_dimen_imovel = self.builder.get_object("entry5")
        self.entry_type_imovel = self.builder.get_object("entry6")
        self.entry_comodos_imovel = self.builder.get_object("entry7")
        self.entry_responsavel_imovel = self.builder.get_object("entry8")
        self.entry_status_imovel = self.builder.get_object("entry9")
        self.entry_data_imovel = self.builder.get_object("entry10")
        self.btn_save_imovel = self.builder.get_object("button6")
        #cadastro compra insumo
        self.janela_cadastro_compra = self.builder.get_object("window5")
        self.entry_imovel_buy_insumo = self.builder.get_object("entry11")
        self.entry_insumo_buy_insumo = self.builder.get_object("entry12")
        self.entry_valor_unity_buy_insumo = self.builder.get_object("entry13")
        self.entry_valor_total_buy_insumo = self.builder.get_object("entry14")
        self.entry_date_buy_insumo = self.builder.get_object("entry15")
        self.btn_save_buy_insumo = self.builder.get_object("button10")
        #operacoes
        self.btn_sel_imovel = self.builder.get_object("button2")
        self.btn_sel_insumo = self.builder.get_object("button3")
        self.btn_sel_buys = self.builder.get_object("button4")
        self.btn_sel_relatorios = self.builder.get_object("button5")
        #selecionar crud
        self.btn_sel_cadastro = self.builder.get_object("button7")
        self.btn_sel_alterar = self.builder.get_object("button8")
        self.btn_sel_remove = self.builder.get_object("button9")

        self.window.connect("delete-event", self.close)

    def open_window(self,window):
        self.window.hide()
        self.window = window
        self.window.show_all()
        self.window.connect("delete-event", self.close)

    def on_button1_clicked(self, button):
        #salvar insumo
        codigo = self.entry_codigo_insumo.get_text()
        descricao = self.entry_descricao_insumo.get_text()
        insumo = self.entry_unity_insumo.get_text()
        if codigo != '' and descricao != '' and insumo != '':
            #salvar
            print(codigo + ' ' + descricao + ' ' + insumo)
            #resetar variaveis
            self.entry_codigo_insumo.set_text('')
            self.entry_descricao_insumo.set_text('')
            self.entry_unity_insumo.set_text('')
            #voltar pra tela inicial
            open_window(self,self.janela_inicio)
    
    def on_button2_clicked(self, button):
        #abrir imóvel
        self.janela = IMOVEL
        open_window(self,self.janela_operacao)

    def on_button3_clicked(self, button):
        #abrir insumo
        self.janela = INSUMO
        open_window(self,self.janela_operacao)

    def on_button4_clicked(self, button):
        #abrir compra insumo
        self.janela = COMPRA_INSUMO
        open_window(self,self.janela_operacao)

    def on_button5_clicked(self, button):
        print('btn5')

    def on_button6_clicked(self, button):
        print('btn6')

    def on_button7_clicked(self, button):
        print('btn7')
        self.window.hide()
        if self.janela == INSUMO:
            #cadastrar insumo
            self.window = self.janela_cadastro_insumo
        elif self.janela == IMOVEL:
            #cadastrar imovel
            self.window = self.janela_cadastro_imovel
        elif self.janela == COMPRA_INSUMO:
            #cadastrar compra
            self.window = self.janela_cadastro_compra
        elif self.janela = RELATORIOS:
            print("relatorios")
        else:
            print("erro inesperado")
        self.window.show_all()
        self.window.connect("delete-event", self.close)

    def on_button8_clicked(self, button):
        print('btn8')

    def on_button9_clicked(self, button):
        print('btn9')

    def on_button10_clicked(self, button):
        print('btn10')

    def close(self, *args):
        Gtk.main_quit(*args)

interface()
Gtk.main()