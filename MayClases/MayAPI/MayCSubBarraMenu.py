#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       MayCSubMenu.py
#       
#       Copyleft 2010 Informática al Alcance de Todos (CA)
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#
import pygame
import os.path
from MayCBoton import MayCBoton

class MayCSubBarraMenu(object):
    def __init__(self,p_Interface_Padre,p_Posicion,p_Tamano,p_Directorio_Recursos_Iconos,p_Tipo='Horizontal',p_Habilitado=True):
        #Inicializo SubMódulos de Pygame
        pygame.init()
        #Propiedades
        self.Interface_Padre=p_Interface_Padre
        self.Tamano=p_Tamano
        self.Posicion_Actual=p_Posicion
        self.Interface=pygame.Surface(p_Tamano,0,32)
        self.Interface.fill((255,255,255))
        self.Tipo=p_Tipo
        self.Directorio_Recursos_Iconos=p_Directorio_Recursos_Iconos    
        #Creacion Items 
        self.SubMenus=[]
        #Boton en Juego (Que esta Interactuando con los eventos =>MOUSEMOTION)
        self.Boton_NJuego=None
        #Variables de Eventos de Raton
        self.Raton_Dentro=False
        self.Raton_Fuera=True
        self.Raton_Click=False
        self.Habilitado=p_Habilitado
            
    def ObtenerInterface(self):
        return self.Interface
        
    def AgregarMensaje(self,p_posicion_mensaje=None):
        if (p_posicion_mensaje==None):
            #Agrego Mensaje tooltip
            self.Boton_NJuego.AgregarMensaje(p_Interface=self.Interface_Padre)        
    
    def QuitarMensaje(self):
        self.ReIniciar(p_QM=True)        
            
    def ReIniciar(self,p_QM=False):
        self.Interface.fill((255,255,255))

        if (p_QM==False):
            self.Raton_Click=False
        
        for contador in range(len(self.SubMenus)):
            self.SubMenus[contador].Insertar()
            
    def Habilitar(self,p_Si_No):
        self.Habilitado=p_Si_No
    
    def InsertarInterface(self):
        self.Interface_Padre.blit(self.Interface,self.Posicion_Actual)                    
        self.InsertarMensajesAyuda()
        
    def InsertarMensajesAyuda(self):
        if(self.Raton_Dentro==True):
            self.AgregarMensaje()
        elif(self.Raton_Fuera==True):
            self.QuitarMensaje()
                    
    def ObtenerPosicion(self):
        return self.Posicion_Actual
        
    def ObtenerTamano(self):
        return self.Tamano    
    
    def CreacionBotones(self,p_IDs,p_Imagenes,p_Mensajes_Ayuda,p_Posicion=(0,0),p_Tamano=(20,10),p_No_SMenus=1):
        posx,posy=p_Posicion
        ancho,alto=p_Tamano
        for contador in range(p_No_SMenus):
            nombre=p_IDs[contador]
            Nombre_Imagen=p_Imagenes[contador]
            Mensaje=p_Mensajes_Ayuda[contador]
            
            if (self.Tipo=='Horizontal'):
                Boton_de_Menu=MayCBoton(self.Interface,nombre,Nombre_Imagen,self.Directorio_Recursos_Iconos,(posx+((ancho+10)*contador),posy),(ancho,alto))
            elif (self.Tipo=='Vertical'):
                Boton_de_Menu=MayCBoton(self.Interface,nombre,Nombre_Imagen,self.Directorio_Recursos_Iconos,(posx,posy+((alto+10)*contador)),(ancho,alto))
                #print nombre + ' ' + str(posy+((alto+10)*contador))
                
            Boton_de_Menu.MensajeAyuda(Mensaje)
            #Agregar Boton a la Interface
            Boton_de_Menu.Insertar()
            self.SubMenus.append(Boton_de_Menu)        
    
    def InsertarMensajesAyuda(self):
        if(self.Raton_Dentro==True):
            self.AgregarMensaje()
        elif(self.Raton_Fuera==True):
            self.QuitarMensaje()
                
    def EvtEntraRaton(self):
        self.Raton_Dentro=True
        self.Raton_Fuera=False
                
    def EvtSaleRaton(self):
        self.Raton_Fuera=True
        self.Raton_Dentro=False
                
    def EvtClick(self):
        #Cuando el Boton es presionado dos veces Raton_Click sera falso y ya no se imprimira el submenu del Boton presionado
        if(self.Raton_Click==False):
              self.Raton_Click=True
              self.Boton_NJuego.Click()
        else:    
              self.Raton_Click=False
                                
    def MovimientoDRaton(self,p_Evento):
        if(self.VerificaEvento(p_Evento)==True):
            Boton=self.BusquedaBoton(p_Evento)
        
            if(self.Raton_Dentro==False and Boton != None):
                self.EvtEntraRaton()
                self.Boton_NJuego.Pos_Mensaje=p_Evento.pos
            elif(self.Raton_Fuera==False and Boton ==None):
                self.EvtSaleRaton()    
            return True    
                            
    def PresionDRaton(self,p_Evento):
        if(self.VerificaEvento(p_Evento)==True):
            Boton=self.BusquedaBoton(p_Evento)
            if(Boton != None):
                self.EvtClick()
                print 'Click en Sub Menu'
            else:
                self.ReIniciar()
            return True    
        else:
               self.ReIniciar()
               return
                                    
    #Busca si se concentra un Posible evento en la Interface
    def VerificaEvento(self,p_evento):
        pos_x2,pos_y2=p_evento.pos
        
        pos_x,pos_y=self.ObtenerPosicion()
        Ancho,Alto=self.ObtenerTamano()
    
        if ((pos_x2>=pos_x and pos_x2<=(pos_x+Ancho)) and (pos_y2>=pos_y and pos_y2<=(pos_y+Alto))):
            return True
        else:
            return False               
    
    def BusquedaBoton(self,evento):        
        for contador in range(len(self.SubMenus)):
            if (self.SubMenus[contador].Busqueda(evento.pos,self.Posicion_Actual)):
                #Boton en Juego
                self.Boton_NJuego=self.SubMenus[contador]
                return self.SubMenus[contador]        
            
    def CPosicion(self,p_posicion):
        self.Posicion_Actual=p_posicion
    
    def CTamano(self,p_tamano):
        self.Tamano=p_tamanos                   