#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# [SNIPPET_NAME: Threaded Server]
# [SNIPPET_CATEGORIES: Python Core, socket, threading]
# [SNIPPET_DESCRIPTION: Simple example of Python's socket and threading modules]
# [SNIPPET_DOCS: http://docs.python.org/library/socket.html, http://docs.python.org/library/threading.html]
# [SNIPPET_AUTHOR: Gonzalo N煤帽ez <gnunezr@gmail.com>]
# [SNIPPET_LICENSE: GPL]

import sys
import socket
import threading
import time

from srl import *

QUIT = False
        
class ClientThread( threading.Thread ):
    ''' 
    Class that implements the client threads in this server
    '''
    print "Loading..."
    e_hownet=EHowNetTree("ehownet_ontology.txt")
    (feature_role_dict_10,feature_role_dict_9,feature_role_dict_8,feature_role_dict_7,feature_role_dict_6,feature_role_dict_5,feature_role_dict_4,feature_role_dict_3,feature_role_dict_2,feature_role_dict_1,legal_roles) = read_model()
    target_pos = get_target_pos()
    pp = get_pp()
    word2semType_dict = word2semType()
    prep_pos = open('./data/tpos.txt').readlines()[2].rstrip().split(',') 
    dummy = 0
    print "Ready!"

    def __init__( self, client_sock ):
        '''
        Initialize the object, save the socket that this thread will use.
        '''

        threading.Thread.__init__( self )
        self.client = client_sock

    def run( self ):
        ''' 
        Thread's main loop. Once this function returns, the thread is finished 
        and dies. 
        '''

        # self.request is the TCP socket connected to the client
        self.data = self.client.recv(1024).strip()
        annotated_tree = self.srl(self.data)
        #print "{} wrote:".format(self.client_address[0])
        # just send back the same data, but upper-cased
        self.client.sendall(annotated_tree)
        #print "Successfully served the request!"
        #
        # Make sure the socket is closed once we're done with it
        #
        self.client.close()
        return

    def srl(self,data):
        clean_expr = data
        #tree = parseExpr_unannotated(clean_expr.encode('utf_8'))
        tree = parseExpr_unannotated(clean_expr)
        passive = isPassive(tree,self.pp,'False')
        annotated_tree = assign_roles(tree,self.e_hownet,self.feature_role_dict_10,self.feature_role_dict_9,self.feature_role_dict_8,self.feature_role_dict_7,self.feature_role_dict_6,self.feature_role_dict_5,self.feature_role_dict_4,self.feature_role_dict_3,self.feature_role_dict_2,self.feature_role_dict_1,self.legal_roles,self.target_pos,passive,self.prep_pos,self.dummy,self.word2semType_dict)
        annotated_tree_line = print_tree_line(annotated_tree,[])
        return ''.join(annotated_tree_line)

    def readline( self ):
        ''' 
        Helper function, reads up to 1024 chars from the socket, and returns 
        them as a string, all letters in lowercase, and without any end of line 
        markers '''

        result = self.client.recv( 1024 )
        if( None != result ):
            result = result.strip().lower()
        return result

    def writeline( self, text ):
        ''' 
        Helper function, writes teh given string to the socket, with an end of 
        line marker appended at the end 
        '''

        self.client.send( text.strip() + '\n' )

class Server:
    ''' 
    Server class. Opens up a socket and listens for incoming connections.
    Every time a new connection arrives, it creates a new ClientThread thread
    object and defers the processing of the connection to it. 
    '''

    def __init__( self ):
        self.sock = None
        self.thread_list = []

    def run( self ):
        '''
        Server main loop. 
        Creates the server (incoming) socket, and listens on it of incoming
        connections. Once an incomming connection is deteceted, creates a 
        ClientThread to handle it, and goes back to listening mode.
        '''
        HOST, PORT = "localhost", 8000

        all_good = False
        try_count = 0

        #
        # Attempt to open the socket
        #
        while not all_good:
            if 3 < try_count:
                #
                # Tried more than 3 times, without success... Maybe the port
                # is in use by another program
                #
                sys.exit( 1 )
            try:
                #
                # Create the socket
                #
                self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
                #
                # Bind it to the interface and port we want to listen on
                #
                self.sock.bind( ( HOST, PORT ) )
                #
                # Listen for incoming connections. This server can handle up to
                # 5 simultaneous connections
                #
                self.sock.listen( 5 )
                all_good = True
                break
            except socket.error, err:
                #
                # Could not bind on the interface and port, wait for 10 seconds
                #
                print 'Socket connection error... Waiting 10 seconds to retry.'
                del self.sock
                time.sleep( 10 )
                try_count += 1

        print "Server is listening for incoming connections."

        try:
            #
            # NOTE - No need to declare QUIT as global, since the method never 
            #    changes its value
            #
            while not QUIT:
                try:
                    #
                    # Wait for half a second for incoming connections
                    #
                    self.sock.settimeout( 0.500 )
                    client = self.sock.accept()[0]
                except socket.timeout:
                    #
                    # No connection detected, sleep for one second, then check
                    # if the global QUIT flag has been set
                    #
                    time.sleep( 1 )
                    if QUIT:
                        print "Received quit command. Shutting down..."
                        break
                    continue
                #
                # Create the ClientThread object and let it handle the incoming
                # connection
                #
                new_thread = ClientThread( client )
                print 'Incoming Connection. Started thread ',
                print new_thread.getName()
                self.thread_list.append( new_thread )
                new_thread.start()

                #
                # Go over the list of threads, remove those that have finished
                # (their run method has finished running) and wait for them 
                # to fully finish
                #
                for thread in self.thread_list:
                    if not thread.isAlive():
                        self.thread_list.remove( thread )
                        thread.join()

        except KeyboardInterrupt:
            print 'Ctrl+C pressed... Shutting Down'
        except Exception, err:
            print 'Exception caught: %s\nClosing...' % err

        #
        # Clear the list of threads, giving each thread 1 second to finish
        # NOTE: There is no guarantee that the thread has finished in the
        #    given time. You should always check if the thread isAlive() after
        #    calling join() with a timeout paramenter to detect if the thread
        #    did finish in the requested time
        #
        for thread in self.thread_list:
            thread.join( 1.0 )
        #
        # Close the socket once we're done with it
        #
        self.sock.close()

if "__main__" == __name__:
    server = Server()
    server.run()

    print "Terminated"