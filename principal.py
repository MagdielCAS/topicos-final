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

    def insert_insumo(self, code,desc,unity):
        cur = self.database.cursor()
        try:
            cur.execute("INSERT INTO insumo VALUES (0,'%s','%s','%s')" % (code, desc, unity))
            self.database.commit()
        except:
            self.database.rollback()

    def insert_imovel(self, end, dim, tipo, qnt_comodos, responsavel,status, data):
        cur = self.database.cursor()
        try:
            cur.execute("INSERT INTO imoveis VALUES (0, '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (end, dim, tipo, qnt_comodos, responsavel,status, data))
            self.database.commit()
        except:
            self.database.rollback()

    def insert_compra(self, insumo, imovel, valoru, valort, data):
        cur = self.database.cursor()
        try:
            cur.execute("INSERT INTO compra_insumo VALUES (%s, %s, '%s', '%s', '%s')" % (insumo, imovel, valoru, valort, data))
            self.database.commit()
        except:
            self.database.rollback()

    def get_insumos(self):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM insumo")
        rows = cur.fetchall()
        return rows

    def get_imoveis(self):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM imoveis")
        rows = cur.fetchall()
        return rows

    def get_compras(self):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM compra_insumo")
        rows = cur.fetchall()
        return rows

    def get_insumo_by_desc(self, desc):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM insumo WHERE descricao = '%s'"% (desc))
        rows = cur.fetchall()
        return rows[0]

    def get_imovel_by_end(self, end):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM imoveis WHERE endereco = '%s'"% (end))
        rows = cur.fetchall()
        return rows[0]

    def get_compra(self, insumo,imovel):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM compra_insumo WHERE insumo = %s AND imoveis = %s"% (insumo,imovel))
        rows = cur.fetchall()
        return rows[0]

    def get_insumo_by_imovel(self,imovel):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM vw_insumo_by_imoveis WHERE imovel = %s"% (imovel))
        rows = cur.fetchall()
        return rows

    def update_insumo_by_desc(self,olddesc,newdesc,newcode,newunity):
        cur = self.database.cursor()
        try:
            cur.execute("UPDATE insumo SET descricao = '%s', codigo = '%s', unity_medida = '%s' WHERE descricao = '%s'" % (newdesc, newcode, newunity, olddesc))
            self.database.commit()
        except:
            self.database.rollback()

    def update_imovel_by_end(self, oldend, end, dim, tipo, qnt_comodos, responsavel,status, data):
        cur = self.database.cursor()
        try:
            cur.execute("UPDATE imoveis SET endereco = '%s', dimensoes = '%s', tipo = '%s', qtd_comodos = '%s', responstavel = '%s', status = '%s', data = '%s' WHERE endereco = '%s'" % (end, dim, tipo, qnt_comodos, responsavel, status, data, oldend))
            self.database.commit()
        except:
            self.database.rollback()

    def update_compra(self, insumo, imovel, valoru, valort, data):
        cur = self.database.cursor()
        try:
            cur.execute("UPDATE compra_insumo SET valor_unitario = '%s', valor_total = '%s', data_compra = '%s' WHERE insumo = %s AND imoveis = %s" % (valoru, valort, data, insumo, imovel))
            self.database.commit()
        except:
            self.database.rollback()

    def remove_insumo(self,desc, codigo, unity):
        cur = self.database.cursor()
        try:
            cur.execute("DELETE FROM insumo WHERE descricao = '%s' AND codigo = '%s' AND unity_medida = '%s'" % (desc, codigo, unity))
            self.database.commit()
        except:
            self.database.rollback()
    
    def remove_imovel(self, end, dim, tipo, qnt_comodos, responsavel, data):
        cur = self.database.cursor()
        try:
            cur.execute("DELETE FROM imoveis WHERE endereco = '%s' AND dimensoes = '%s' AND tipo = '%s' AND qtd_comodos = '%s' AND responstavel = '%s' AND data = '%s'" % (end, dim, tipo, qnt_comodos, responsavel, data))
            self.database.commit()
        except:
            self.database.rollback()

    def remove_compra(self,insumo,imovel):
        cur = self.database.cursor()
        try:
            cur.execute("DELETE FROM compra_insumo WHERE insumo = %s AND imoveis = %s" % (insumo, imovel))
            self.database.commit()
        except:
            self.database.rollback()

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
        self.janela_relatorio = self.builder.get_object("window14")
        self.janela_relatorio_imovel = self.builder.get_object("window12")
        self.janela_relatorio_compra = self.builder.get_object("window13")
        self.janela_relatorio_insumo = self.builder.get_object("window15")
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
        #imovel
        ##janelas
        self.janela_cadastro_imovel = self.builder.get_object("window4")
        self.janela_alterar_imovel = self.builder.get_object("window8")
        self.janela_remover_imovel = self.builder.get_object("window9")
        ##entradas cadastro
        self.entry_endereco_imovel = self.builder.get_object("entry4")
        self.entry_dimen_imovel = self.builder.get_object("entry5")
        self.entry_type_imovel = self.builder.get_object("entry6")
        self.entry_comodos_imovel = self.builder.get_object("entry7")
        self.entry_responsavel_imovel = self.builder.get_object("entry8")
        self.entry_status_imovel = self.builder.get_object("entry9")
        self.entry_data_imovel = self.builder.get_object("entry10")
        ##entradas edit
        self.combo_imovel_edit = self.builder.get_object("combobox3")
        self.entry_endereco_imovel_edit = self.builder.get_object("entry19")
        self.entry_dimen_imovel_edit = self.builder.get_object("entry20")
        self.entry_type_imovel_edit = self.builder.get_object("entry21")
        self.entry_comodos_imovel_edit = self.builder.get_object("entry22")
        self.entry_responsavel_imovel_edit = self.builder.get_object("entry23")
        self.entry_status_imovel_edit = self.builder.get_object("entry24")
        self.entry_data_imovel_edit = self.builder.get_object("entry25")
        ##labels remove
        self.combo_imovel_remove = self.builder.get_object("combobox4")
        self.label_endereco_imovel_remove = self.builder.get_object("label52")
        self.label_dimen_imovel_remove = self.builder.get_object("label53")
        self.label_type_imovel_remove = self.builder.get_object("label54")
        self.label_comodos_imovel_remove = self.builder.get_object("label55")
        self.label_responsavel_imovel_remove = self.builder.get_object("label56")
        self.label_status_imovel_remove = self.builder.get_object("label57")
        self.label_data_imovel_remove = self.builder.get_object("label58")
        #compra insumo
        ##janelas
        self.janela_cadastro_compra = self.builder.get_object("window5")
        self.janela_alterar_compra = self.builder.get_object("window10")
        self.janela_remover_compra = self.builder.get_object("window11")
        ##entradas cadastro
        self.combo_imovel_buy_insumo = self.builder.get_object("combobox7")
        self.combo_insumo_buy_insumo = self.builder.get_object("combobox8")
        self.entry_valor_unity_buy_insumo = self.builder.get_object("entry13")
        self.entry_valor_total_buy_insumo = self.builder.get_object("entry14")
        self.entry_date_buy_insumo = self.builder.get_object("entry15")
        ##entradas edit
        self.combo_imovel_buy_insumo_edit = self.builder.get_object("combobox9")
        self.combo_insumo_buy_insumo_edit = self.builder.get_object("combobox10")
        self.entry_valor_unity_buy_insumo_edit = self.builder.get_object("entry28")
        self.entry_valor_total_buy_insumo_edit = self.builder.get_object("entry29")
        self.entry_date_buy_insumo_edit = self.builder.get_object("entry30")
        ##labels remove
        self.combo_imovel_buy_insumo_remove = self.builder.get_object("combobox6")
        self.combo_insumo_buy_insumo_remove = self.builder.get_object("combobox11")
        self.label_valor_unity_buy_insumo_remove = self.builder.get_object("label75")
        self.label_valor_total_buy_insumo_remove = self.builder.get_object("label76")
        self.label_date_buy_insumo_remove = self.builder.get_object("label77")
        #consulta imovel
        self.combo_imovel = self.builder.get_object("combobox5")
        self.label_endereco_imovel = self.builder.get_object("label82")
        self.label_dimen_imovel = self.builder.get_object("label83")
        self.label_type_imovel = self.builder.get_object("label84")
        self.label_comodos_imovel = self.builder.get_object("label85")
        self.label_responsavel_imovel = self.builder.get_object("label86")
        self.label_status_imovel = self.builder.get_object("label87")
        self.label_data_imovel = self.builder.get_object("label88")
        #consulta compra
        self.combo_imovel_buy_insumo_consult = self.builder.get_object("combobox12")
        self.combo_insumo_buy_insumo_consult = self.builder.get_object("combobox13")
        self.label_valor_unity_buy_insumo_consult = self.builder.get_object("label95")
        self.label_valor_total_buy_insumo_consult = self.builder.get_object("label96")
        self.label_date_buy_insumo_consult = self.builder.get_object("label97")
        #consulta insumo
        self.combo_insumo_consult = self.builder.get_object("combobox14")
        self.label_codigo_insumo_consult = self.builder.get_object("label104")
        self.label_descricao_insumo_consult = self.builder.get_object("label105")
        self.label_unity_insumo_consult = self.builder.get_object("label106")

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
        unity = self.entry_unity_insumo.get_text()
        if codigo != '' and descricao != '' and unity != '':
            #salvar
            self.db.insert_insumo(codigo,descricao,unity)
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
        self.open_window(self.janela_relatorio)

    def on_button6_clicked(self, button):
        #salvar cadastro imovel
        end = self.entry_endereco_imovel.get_text()
        dimen = self.entry_dimen_imovel.get_text()
        tipo = self.entry_type_imovel.get_text()
        qnt_comodo = self.entry_comodos_imovel.get_text()
        responsavel = self.entry_responsavel_imovel.get_text()
        status = self.entry_status_imovel.get_text()
        data = self.entry_data_imovel.get_text()
        
        if end != '' and dimen != '' and tipo != '' and qnt_comodo != '' and responsavel != '' and status != '' and data != '':
            #salvar
            self.db.insert_imovel(end, dimen, tipo, qnt_comodo, responsavel, status, data)
            #resetar variaveis
            self.entry_endereco_imovel.set_text('')
            self.entry_dimen_imovel.set_text('')
            self.entry_type_imovel.set_text('')
            self.entry_comodos_imovel.set_text('')
            self.entry_responsavel_imovel.set_text('')
            self.entry_status_imovel.set_text('')
            self.entry_data_imovel.set_text('')
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
            model = self.combo_imovel_buy_insumo.get_model()
            if model is None:
                model = Gtk.ListStore(str)
                renderer_text = Gtk.CellRendererText()
                self.combo_imovel_buy_insumo.pack_start(renderer_text, True)
                self.combo_imovel_buy_insumo.add_attribute(renderer_text, "text", 0)
            self.combo_imovel_buy_insumo.set_model(None)
            model.clear()
            imoveis = self.db.get_imoveis()
            for imovel in imoveis:
                model.append([imovel[1]])    
            self.combo_imovel_buy_insumo.set_model(model)
            model = self.combo_insumo_buy_insumo.get_model()
            if model is None:
                model = Gtk.ListStore(str)
                renderer_text = Gtk.CellRendererText()
                self.combo_insumo_buy_insumo.pack_start(renderer_text, True)
                self.combo_insumo_buy_insumo.add_attribute(renderer_text, "text", 0)
            self.combo_insumo_buy_insumo.set_model(None)
            model.clear()
            insumos = self.db.get_insumos()
            for insumo in insumos:
                model.append([insumo[2]])    
            self.combo_insumo_buy_insumo.set_model(model)
            self.window = self.janela_cadastro_compra
        else:
            print("erro inesperado")
        self.window.show_all()
        self.window.connect("delete-event", self.close)

    def on_button8_clicked(self, button):
        #Alterar
        self.window.hide()
        if self.janela == INSUMO:
            #alterar insumo
            model = self.combo_insumo_edit.get_model()
            if model is None:
                model = Gtk.ListStore(str)
                renderer_text = Gtk.CellRendererText()
                self.combo_insumo_edit.pack_start(renderer_text, True)
                self.combo_insumo_edit.add_attribute(renderer_text, "text", 0)
            self.combo_insumo_edit.set_model(None)
            model.clear()
            insumos = self.db.get_insumos()
            for insumo in insumos:
                model.append([insumo[2]])    
            self.combo_insumo_edit.set_model(model)
            self.window = self.janela_alterar_insumo
        elif self.janela == IMOVEL:
            #alterar imovel
            model = self.combo_imovel_edit.get_model()
            if model is None:
                model = Gtk.ListStore(str)
                renderer_text = Gtk.CellRendererText()
                self.combo_imovel_edit.pack_start(renderer_text, True)
                self.combo_imovel_edit.add_attribute(renderer_text, "text", 0)
            self.combo_imovel_edit.set_model(None)
            model.clear()
            imoveis = self.db.get_imoveis()
            for imovel in imoveis:
                model.append([imovel[1]])    
            self.combo_imovel_edit.set_model(model)
            self.window = self.janela_alterar_imovel
        elif self.janela == COMPRA_INSUMO:
            #alterar compra
            model = self.combo_imovel_buy_insumo_edit.get_model()
            if model is None:
                model = Gtk.ListStore(str)
                renderer_text = Gtk.CellRendererText()
                self.combo_imovel_buy_insumo_edit.pack_start(renderer_text, True)
                self.combo_imovel_buy_insumo_edit.add_attribute(renderer_text, "text", 0)
            self.combo_imovel_buy_insumo_edit.set_model(None)
            model.clear()
            imoveis = self.db.get_imoveis()
            for imovel in imoveis:
                model.append([imovel[1]])    
            self.combo_imovel_buy_insumo_edit.set_model(model)
            self.window = self.janela_alterar_compra
        else:
            print("erro inesperado")
        self.window.show_all()
        self.window.connect("delete-event", self.close)

    def on_button9_clicked(self, button):
        #remover
        self.window.hide()
        if self.janela == INSUMO:
            #remover insumo
            model = self.combo_insumo_remove.get_model()
            if model is None:
                model = Gtk.ListStore(str)
                renderer_text = Gtk.CellRendererText()
                self.combo_insumo_remove.pack_start(renderer_text, True)
                self.combo_insumo_remove.add_attribute(renderer_text, "text", 0)
            self.combo_insumo_remove.set_model(None)
            model.clear()
            insumos = self.db.get_insumos()
            for insumo in insumos:
                model.append([insumo[2]])    
            self.combo_insumo_remove.set_model(model)
            self.window = self.janela_remover_insumo
        elif self.janela == IMOVEL:
            #remover imovel
            model = self.combo_imovel_remove.get_model()
            if model is None:
                model = Gtk.ListStore(str)
                renderer_text = Gtk.CellRendererText()
                self.combo_imovel_remove.pack_start(renderer_text, True)
                self.combo_imovel_remove.add_attribute(renderer_text, "text", 0)
            self.combo_imovel_remove.set_model(None)
            model.clear()
            imoveis = self.db.get_imoveis()
            for imovel in imoveis:
                model.append([imovel[1]])    
            self.combo_imovel_remove.set_model(model)
            self.window = self.janela_remover_imovel
        elif self.janela == COMPRA_INSUMO:
            #remover compra
            model = self.combo_imovel_buy_insumo_remove.get_model()
            if model is None:
                model = Gtk.ListStore(str)
                renderer_text = Gtk.CellRendererText()
                self.combo_imovel_buy_insumo_remove.pack_start(renderer_text, True)
                self.combo_imovel_buy_insumo_remove.add_attribute(renderer_text, "text", 0)
            self.combo_imovel_buy_insumo_remove.set_model(None)
            model.clear()
            imoveis = self.db.get_imoveis()
            for imovel in imoveis:
                model.append([imovel[1]])    
            self.combo_imovel_buy_insumo_remove.set_model(model)
            self.window = self.janela_remover_compra
        else:
            print("erro inesperado")
        self.window.show_all()
        self.window.connect("delete-event", self.close)

    def on_button10_clicked(self, button):
        #salvar cadastro compra
        #voltar pra tela inicial
        self.db.insert_compra(self.selected_insumo_buy, self.selected_imovel_buy, self.entry_valor_unity_buy_insumo.get_text(), self.entry_valor_total_buy_insumo.get_text(), self.entry_date_buy_insumo.get_text())
        self.selected_insumo_buy = 0
        self.selected_imovel_buy = 0
        self.entry_valor_unity_buy_insumo.set_text('')
        self.entry_valor_total_buy_insumo.set_text('')
        self.entry_date_buy_insumo.set_text('')
        self.open_window(self.janela_inicio)
    
    def on_button11_clicked(self, button):
        #salvar alterar insumo
        self.db.update_insumo_by_desc(self.selected_insumo,self.entry_descricao_insumo_edit.get_text(),self.entry_codigo_insumo_edit.get_text(),self.entry_unity_insumo_edit.get_text())
        self.selected_insumo = ''
        self.entry_descricao_insumo_edit.set_text('')
        self.entry_codigo_insumo_edit.set_text('')
        self.entry_unity_insumo_edit.set_text('')
        self.open_window(self.janela_inicio)
    
    def on_button12_clicked(self, button):
        #remover insumo
        self.db.remove_insumo(self.label_descricao_insumo_remove.get_text(),self.label_codigo_insumo_remove.get_text(),self.label_unity_insumo_remove.get_text())
        self.selected_insumo = ''
        self.label_descricao_insumo_remove.set_text('')
        self.label_codigo_insumo_remove.set_text('')
        self.label_unity_insumo_remove.set_text('')
        self.open_window(self.janela_inicio)

    def on_button13_clicked(self, button):
        #salvar editar imovel
        self.db.update_imovel_by_end(self.selected_imovel,self.entry_endereco_imovel_edit.get_text(), self.entry_dimen_imovel_edit.get_text(), self.entry_type_imovel_edit.get_text(), self.entry_comodos_imovel_edit.get_text(), self.entry_responsavel_imovel_edit.get_text(), self.entry_status_imovel_edit.get_text(),self.entry_data_imovel_edit.get_text())
        self.selected_imovel = ''
        self.entry_endereco_imovel_edit.set_text('')
        self.entry_dimen_imovel_edit.set_text('')
        self.entry_type_imovel_edit.set_text('')
        self.entry_comodos_imovel_edit.set_text('')
        self.entry_responsavel_imovel_edit.set_text('')
        self.entry_status_imovel_edit.set_text('')
        self.entry_data_imovel_edit.set_text('')
        self.open_window(self.janela_inicio)

    def on_button14_clicked(self, button):
        #remover imovel
        self.db.remove_imovel(self.label_endereco_imovel_remove.get_text(), self.label_dimen_imovel_remove.get_text(), self.label_type_imovel_remove.get_text(), self.label_comodos_imovel_remove.get_text(), self.label_responsavel_imovel_remove.get_text(), self.label_data_imovel_remove.get_text())
        self.selected_imovel = ''
        self.label_endereco_imovel_remove.set_text('')
        self.label_dimen_imovel_remove.set_text('')
        self.label_type_imovel_remove.set_text('')
        self.label_comodos_imovel_remove.set_text('')
        self.label_responsavel_imovel_remove.set_text('')
        self.label_status_imovel_remove.set_text('')
        self.label_data_imovel_remove.set_text('')
        self.open_window(self.janela_inicio)
    
    def on_button15_clicked(self, button):
        #salvar editar compra
        #voltar pra tela inicial
        self.db.update_compra(self.selected_insumo_buy, self.selected_imovel_buy, self.entry_valor_unity_buy_insumo_edit.get_text(), self.entry_valor_total_buy_insumo_edit.get_text(), self.entry_date_buy_insumo_edit.get_text())
        self.selected_insumo_buy = 0
        self.selected_imovel_buy = 0
        self.entry_valor_unity_buy_insumo_edit.set_text('')
        self.entry_valor_total_buy_insumo_edit.set_text('')
        self.entry_date_buy_insumo_edit.set_text('')
        self.open_window(self.janela_inicio)

    def on_button16_clicked(self, button):
        #remover compra
        #voltar pra tela inicial
        self.db.remove_compra(self.selected_insumo_buy, self.selected_imovel_buy)
        self.selected_insumo_buy = 0
        self.selected_imovel_buy = 0
        self.label_valor_unity_buy_insumo_remove.set_text('')
        self.label_valor_total_buy_insumo_remove.set_text('')
        self.label_date_buy_insumo_remove.set_text('')
        self.open_window(self.janela_inicio)

    def on_button17_clicked(self, button):
        #voltar consulta imoveis
        self.label_endereco_imovel.set_text('')
        self.label_dimen_imovel.set_text('')
        self.label_type_imovel.set_text('')
        self.label_comodos_imovel.set_text('')
        self.label_responsavel_imovel.set_text('')
        self.label_data_imovel.set_text('')
        self.label_status_imovel.set_text('')
        self.open_window(self.janela_inicio)

    def on_button18_clicked(self, button):
        #voltar consulta compra
        self.label_valor_unity_buy_insumo_consult.set_text('')
        self.label_valor_total_buy_insumo_consult.set_text('')
        self.label_date_buy_insumo_consult.set_text('')
        self.open_window(self.janela_inicio)
    
    def on_button19_clicked(self, button):
        #abrir consulta de imoveis
        model = self.combo_imovel.get_model()
        if model is None:
            model = Gtk.ListStore(str)
            renderer_text = Gtk.CellRendererText()
            self.combo_imovel.pack_start(renderer_text, True)
            self.combo_imovel.add_attribute(renderer_text, "text", 0)
        self.combo_imovel.set_model(None)
        model.clear()
        imoveis = self.db.get_imoveis()
        for imovel in imoveis:
            model.append([imovel[1]])    
        self.combo_imovel.set_model(model)
        self.open_window(self.janela_relatorio_imovel)

    def on_button20_clicked(self, button):
        #abrir consulta de compras
        model = self.combo_imovel_buy_insumo_consult.get_model()
        if model is None:
            model = Gtk.ListStore(str)
            renderer_text = Gtk.CellRendererText()
            self.combo_imovel_buy_insumo_consult.pack_start(renderer_text, True)
            self.combo_imovel_buy_insumo_consult.add_attribute(renderer_text, "text", 0)
        self.combo_imovel_buy_insumo_consult.set_model(None)
        model.clear()
        imoveis = self.db.get_imoveis()
        for imovel in imoveis:
            model.append([imovel[1]])    
        self.combo_imovel_buy_insumo_consult.set_model(model)
        self.open_window(self.janela_relatorio_compra)

    def on_button21_clicked(self, button):
        #voltar
        self.open_window(self.janela_inicio)

    def on_button22_clicked(self, button):
        #consulta insumo
        model = self.combo_insumo_consult.get_model()
        if model is None:
            model = Gtk.ListStore(str)
            renderer_text = Gtk.CellRendererText()
            self.combo_insumo_consult.pack_start(renderer_text, True)
            self.combo_insumo_consult.add_attribute(renderer_text, "text", 0)
        self.combo_insumo_consult.set_model(None)
        model.clear()
        insumos = self.db.get_insumos()
        for insumo in insumos:
            model.append([insumo[2]])    
        self.combo_insumo_consult.set_model(model)
        self.open_window(self.janela_relatorio_insumo)

    def on_button23_clicked(self, button):
        #voltar consulta insumo
        self.label_valor_total_buy_insumo_consult.set_text('')
        self.label_valor_unity_buy_insumo_consult.set_text('')
        self.label_date_buy_insumo_consult.set_text('')
        self.open_window(self.janela_inicio)

    def on_combobox1_changed(self, combo):
        #combo alterar insumo
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            desc = model[tree_iter][0]
            atributes = self.db.get_insumo_by_desc(desc)
            self.entry_codigo_insumo_edit.set_text(atributes[1])
            self.entry_descricao_insumo_edit.set_text(atributes[2])
            self.entry_unity_insumo_edit.set_text(atributes[3])
            self.selected_insumo = desc
    
    def on_combobox2_changed(self, combo):
        #combo remover insumo
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            desc = model[tree_iter][0]
            atributes = self.db.get_insumo_by_desc(desc)
            self.label_codigo_insumo_remove.set_text(atributes[1])
            self.label_descricao_insumo_remove.set_text(atributes[2])
            self.label_unity_insumo_remove.set_text(atributes[3])
            self.selected_insumo = desc

    def on_combobox3_changed(self, combo):
        #combo remover imovel
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            desc = model[tree_iter][0]
            atributes = self.db.get_imovel_by_end(desc)
            self.entry_endereco_imovel_edit.set_text(atributes[1])
            self.entry_dimen_imovel_edit.set_text(atributes[2])
            self.entry_type_imovel_edit.set_text(atributes[3])
            self.entry_comodos_imovel_edit.set_text(atributes[4])
            self.entry_responsavel_imovel_edit.set_text(atributes[5])
            self.entry_data_imovel_edit.set_text(atributes[6])
            self.entry_status_imovel_edit.set_text(atributes[7])
            self.selected_imovel = desc

    def on_combobox4_changed(self, combo):
        #combo remover imovel
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            desc = model[tree_iter][0]
            atributes = self.db.get_imovel_by_end(desc)
            self.label_endereco_imovel_remove.set_text(atributes[1])
            self.label_dimen_imovel_remove.set_text(atributes[2])
            self.label_type_imovel_remove.set_text(atributes[3])
            self.label_comodos_imovel_remove.set_text(atributes[4])
            self.label_responsavel_imovel_remove.set_text(atributes[5])
            self.label_data_imovel_remove.set_text(atributes[6])
            self.label_status_imovel_remove.set_text(atributes[7])
            self.selected_imovel = desc

    def on_combobox5_changed(self, combo):
        #selecionar imovel
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            desc = model[tree_iter][0]
            atributes = self.db.get_imovel_by_end(desc)
            self.label_endereco_imovel.set_text(atributes[1])
            self.label_dimen_imovel.set_text(atributes[2])
            self.label_type_imovel.set_text(atributes[3])
            self.label_comodos_imovel.set_text(atributes[4])
            self.label_responsavel_imovel.set_text(atributes[5])
            self.label_data_imovel.set_text(atributes[6])
            self.label_status_imovel.set_text(atributes[7])

    def on_combobox6_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            desc = model[tree_iter][0]
            atributes = self.db.get_imovel_by_end(desc)
            self.selected_imovel_buy = atributes[0]
            model = self.combo_insumo_buy_insumo_remove.get_model()
            if model is None:
                model = Gtk.ListStore(str)
                renderer_text = Gtk.CellRendererText()
                self.combo_insumo_buy_insumo_remove.pack_start(renderer_text, True)
                self.combo_insumo_buy_insumo_remove.add_attribute(renderer_text, "text", 0)
            self.combo_insumo_buy_insumo_remove.set_model(None)
            model.clear()
            insumos = self.db.get_insumo_by_imovel(self.selected_imovel_buy)
            for insumo in insumos:
                model.append([insumo[1]])    
            self.combo_insumo_buy_insumo_remove.set_model(model)
    
    def on_combobox7_changed(self, combo):
        #combo selecionar imovel compra
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            desc = model[tree_iter][0]
            atributes = self.db.get_imovel_by_end(desc)
            self.selected_imovel_buy = atributes[0]

    def on_combobox8_changed(self, combo):
        #combo selecionar insumo compra
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            desc = model[tree_iter][0]
            atributes = self.db.get_insumo_by_desc(desc)
            self.selected_insumo_buy = atributes[0]

    def on_combobox9_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            desc = model[tree_iter][0]
            atributes = self.db.get_imovel_by_end(desc)
            self.selected_imovel_buy = atributes[0]
            model = self.combo_insumo_buy_insumo_edit.get_model()
            if model is None:
                model = Gtk.ListStore(str)
                renderer_text = Gtk.CellRendererText()
                self.combo_insumo_buy_insumo_edit.pack_start(renderer_text, True)
                self.combo_insumo_buy_insumo_edit.add_attribute(renderer_text, "text", 0)
            self.combo_insumo_buy_insumo_edit.set_model(None)
            model.clear()
            insumos = self.db.get_insumo_by_imovel(self.selected_imovel_buy)
            for insumo in insumos:
                model.append([insumo[1]])    
            self.combo_insumo_buy_insumo_edit.set_model(model)
    
    def on_combobox10_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            desc = model[tree_iter][0]
            atributes = self.db.get_insumo_by_desc(desc)
            self.selected_insumo_buy = atributes[0]

    def on_combobox11_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            desc = model[tree_iter][0]
            atributes = self.db.get_insumo_by_desc(desc)
            self.selected_insumo_buy = atributes[0]
            data = self.db.get_compra(self.selected_insumo_buy,self.selected_imovel_buy)
            self.label_valor_unity_buy_insumo_remove.set_text(data[2])
            self.label_valor_total_buy_insumo_remove.set_text(data[3])
            self.label_date_buy_insumo_remove.set_text(data[4])

    def on_combobox12_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            desc = model[tree_iter][0]
            atributes = self.db.get_imovel_by_end(desc)
            selected_imovel_consult = atributes[0]
            model = self.combo_insumo_buy_insumo_consult.get_model()
            if model is None:
                model = Gtk.ListStore(str)
                renderer_text = Gtk.CellRendererText()
                self.combo_insumo_buy_insumo_consult.pack_start(renderer_text, True)
                self.combo_insumo_buy_insumo_consult.add_attribute(renderer_text, "text", 0)
            self.combo_insumo_buy_insumo_consult.set_model(None)
            model.clear()
            insumos = self.db.get_insumo_by_imovel(selected_imovel_consult)
            for insumo in insumos:
                model.append([insumo[1]])    
            self.combo_insumo_buy_insumo_consult.set_model(model)
    
    def on_combobox13_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            desc = model[tree_iter][0]
            atributes = self.db.get_insumo_by_desc(desc)
            self.selected_insumo_buy = atributes[0]
            self.label_valor_unity_buy_insumo_consult.set_text(atributes[1])
            self.label_valor_total_buy_insumo_consult.set_text(atributes[2])
            self.label_date_buy_insumo_consult.set_text(atributes[3])
    
    def on_combobox14_changed(self, combo):
        #combo consultar insumo
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            desc = model[tree_iter][0]
            atributes = self.db.get_insumo_by_desc(desc)
            self.label_codigo_insumo_consult.set_text(atributes[1])
            self.label_descricao_insumo_consult.set_text(atributes[2])
            self.label_unity_insumo_consult.set_text(atributes[3])

    def close(self, *args):
        Gtk.main_quit(*args)

interface()
Gtk.main()