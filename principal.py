import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import MySQLdb as mdb
import sys

INICIO = 'inicio'
INSUMO = 'insumo'
IMOVEL = 'imovel'
COMPRA_INSUMO = 'compra_insumo'
RELATORIOS = 'relatorios'

class database:
    def __init__(self):
        try:
            self.database = mdb.connect(user = "root",passwd="root",db="mydb")
        except mdb.Error as err:
            print(err)
    
    def get_insumos(self):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM insumo")
        rows = cur.fetchall()
        return rows

class interface:
    def __init__(self):
        self.db = database()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("interface.glade")
        self.builder.connect_signals(self)

        #janela principal
        self.window = self.builder.get_object("window2")
        self.window.show_all()
        self.janela = INICIO

        #Objetos
        ##janelas
        self.janela_inicio = self.builder.get_object("window2")
        self.janela_operacao = self.builder.get_object("window3")
        #insumo
        ##janelas
        self.janela_cadastro_insumo = self.builder.get_object("window1")
        self.janela_alterar_insumo = self.builder.get_object("window6")
        self.janela_remover_insumo = self.builder.get_object("window7")
        ##entradas cadastro
        self.entry_codigo_insumo = self.builder.get_object("entry1")
        self.entry_descricao_insumo = self.builder.get_object("entry2")
        self.entry_unity_insumo = self.builder.get_object("entry3")
        ##entradas edit
        self.combo_insumo_edit = self.builder.get_object("combobox1")
        self.entry_codigo_insumo_edit = self.builder.get_object("entry16")
        self.entry_descricao_insumo_edit = self.builder.get_object("entry17")
        self.entry_unity_insumo_edit = self.builder.get_object("entry18")
        ##labels remove
        self.combo_insumo_remove = self.builder.get_object("combobox2")
        self.label_codigo_insumo_remove = self.builder.get_object("label31")
        self.label_descricao_insumo_remove = self.builder.get_object("label32")
        self.label_unity_insumo_remove = self.builder.get_object("label33")
        ##buttons
        self.btn_save_cadastro_insumo = self.builder.get_object("button1")
        self.btn_save_alterar_insumo = self.builder.get_object("button11")
        self.btn_save_remover_insumo = self.builder.get_object("button12")
        #imovel
        ##janelas
        self.janela_cadastro_imovel = self.builder.get_object("window4")
        self.janela_alterar_imovel = self.builder.get_object("window8")
        self.janela_remover_imovel = self.builder.get_object("window9")
        self.entry_endereco_imovel = self.builder.get_object("entry4")
        self.entry_dimen_imovel = self.builder.get_object("entry5")
        self.entry_type_imovel = self.builder.get_object("entry6")
        self.entry_comodos_imovel = self.builder.get_object("entry7")
        self.entry_responsavel_imovel = self.builder.get_object("entry8")
        self.entry_status_imovel = self.builder.get_object("entry9")
        self.entry_data_imovel = self.builder.get_object("entry10")
        self.btn_save_cadastro_imovel = self.builder.get_object("button6")
        self.btn_save_alterar_imovel = self.builder.get_object("button13")
        self.btn_save_remover_imovel = self.builder.get_object("button14")
        #compra insumo
        ##janelas
        self.janela_cadastro_compra = self.builder.get_object("window5")
        self.janela_alterar_compra = self.builder.get_object("window10")
        self.janela_remover_compra = self.builder.get_object("window11")
        self.entry_imovel_buy_insumo = self.builder.get_object("entry11")
        self.entry_insumo_buy_insumo = self.builder.get_object("entry12")
        self.entry_valor_unity_buy_insumo = self.builder.get_object("entry13")
        self.entry_valor_total_buy_insumo = self.builder.get_object("entry14")
        self.entry_date_buy_insumo = self.builder.get_object("entry15")
        self.btn_save_cadastro_buy_insumo = self.builder.get_object("button10")
        self.btn_save_alterar_buy_insumo = self.builder.get_object("button15")
        self.btn_save_remover_buy_insumo = self.builder.get_object("button16")
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
            self.open_window(self.janela_inicio)
    
    def on_button2_clicked(self, button):
        #abrir imovel
        self.janela = IMOVEL
        self.open_window(self.janela_operacao)

    def on_button3_clicked(self, button):
        #abrir insumo
        self.janela = INSUMO
        self.open_window(self.janela_operacao)

    def on_button4_clicked(self, button):
        #abrir compra insumo
        self.janela = COMPRA_INSUMO
        self.open_window(self.janela_operacao)

    def on_button5_clicked(self, button):
        #abrir relatorios
        self.janela = RELATORIOS
        self.open_window(self.janela_operacao)

    def on_button6_clicked(self, button):
        #salvar cadastro imovel
        #voltar pra tela inicial
        self.open_window(self.janela_inicio)

    def on_button7_clicked(self, button):
        #cadastrar
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
        elif self.janela == RELATORIOS:
            print("relatorios")
            self.window = self.janela_inicio
        else:
            print("erro inesperado")
        self.window.show_all()
        self.window.connect("delete-event", self.close)

    def on_button8_clicked(self, button):
        #Alterar
        self.window.hide()
        if self.janela == INSUMO:
            #alterar insumo
            model = Gtk.ListStore(str)
            insumos = self.db.get_insumos()
            for insumo in insumos:
                model.append([insumo[1]])    
            self.combo_insumo_edit.set_model(model)
            renderer_text = Gtk.CellRendererText()
            self.combo_insumo_edit.pack_start(renderer_text, True)
            self.combo_insumo_edit.add_attribute(renderer_text, "text", 0)
            self.window = self.janela_alterar_insumo
        elif self.janela == IMOVEL:
            #alterar imovel
            self.window = self.janela_alterar_imovel
        elif self.janela == COMPRA_INSUMO:
            #alterar compra
            self.window = self.janela_alterar_compra
        elif self.janela == RELATORIOS:
            print("relatorios")
            self.window = self.janela_inicio
        else:
            print("erro inesperado")
        self.window.show_all()
        self.window.connect("delete-event", self.close)

    def on_button9_clicked(self, button):
        #remover
        self.window.hide()
        if self.janela == INSUMO:
            #remover insumo
            list_store = Gtk.ListStore(gobject.TYPE_STRING)
            insumos = self.db.get_insumos()
            for insumo in insumos:
                list_store.append(insumo[1])
            self.combo_insumo_remove.set_model(list_store)
            self.combo_insumo_remove.set_active(0)
            # And here's the new stuff:
            cell = Gtk.CellRendererText()
            self.combo_insumo_remove.pack_start(cell, True)
            self.combo_insumo_remove.add_attribute(cell, "text", 0)
            self.window = self.janela_remover_insumo
        elif self.janela == IMOVEL:
            #remover imovel
            self.window = self.janela_remover_imovel
        elif self.janela == COMPRA_INSUMO:
            #remover compra
            self.window = self.janela_remover_compra
        elif self.janela == RELATORIOS:
            print("relatorios")
            self.window = self.janela_inicio
        else:
            print("erro inesperado")
        self.window.show_all()
        self.window.connect("delete-event", self.close)

    def on_button10_clicked(self, button):
        #salvar cadastro compra
        #voltar pra tela inicial
        self.open_window(self.janela_inicio)
    
    def on_button11_clicked(self, button):
        #salvar alterar insumo
        #voltar pra tela inicial
        self.open_window(self.janela_inicio)
    
    def on_button12_clicked(self, button):
        #remover insumo
        #voltar pra tela inicial
        self.open_window(self.janela_inicio)

    def on_button13_clicked(self, button):
        #salvar editar imovel
        #voltar pra tela inicial
        self.open_window(self.janela_inicio)

    def on_button14_clicked(self, button):
        #remover imovel
        #voltar pra tela inicial
        self.open_window(self.janela_inicio)
    
    def on_button15_clicked(self, button):
        #salvar editar compra
        #voltar pra tela inicial
        self.open_window(self.janela_inicio)

    def on_button16_clicked(self, button):
        #remover compra
        #voltar pra tela inicial
        self.open_window(self.janela_inicio)

    def close(self, *args):
        Gtk.main_quit(*args)

interface()
Gtk.main()