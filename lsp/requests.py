
class Requests:

    def __init__(self):
        self.jsonrpc = "2.0"

    def getShutdownRequest(self):
        return {
            "jsonrpc": self.jsonrpc,
            "id": 0,
            "method": "shutdown",
            "params": {}
        }

    def getExitRequest(self):
        return {
            "jsonrpc": self.jsonrpc,
            "method": "exit",
            "params": {}
        }

    def getInitializeRequest(self, process_id):
        return {
            "jsonrpc": self.jsonrpc,
            "id": 0,
            "method": "initialize",
            "params": {
                "processId": process_id,
                "rootUri": None,
                "capabilities": {
                    "completionProvider":
                    {
                        "resolveProvider": True
                    },
                    "textDocument": {
                        "hover":
                        {
                            "dynamicRegistration": False
                        },
                        "diagnostics":{
                            "dynamicRegistration": False, 
                            "relatedDocumentSupport": False,
                        },
                        "publishDiagnostics": True,
                        "completion": {"dynamicRegistration": True},
                        "synchronization": {
                            "dynamicRegistration": True,
                            "willSave": False,
                            "willSaveWaitUntil": False,
                            "didSave": False
                        }
                    }
                }
            }
        }

    def getOpenDocument(self, uri, text, version):
        return {
            "jsonrpc": self.jsonrpc,
            "method": "textDocument/didOpen",
            "params": {
                "textDocument": {
                    "uri": uri,
                    "languageId": "cpp",
                    "version": version,
                    "text": text
                }
            }
        }

    def getInitializedRequest(self):
        return {
            "jsonrpc": self.jsonrpc,
            "method": "initialized",
            "params": {}
        }

    def changeNotification(self, text, uri, version):
        return {
            "jsonrpc": self.jsonrpc,
            "method": "textDocument/didChange",
            "params": {
                "textDocument": {
                    "uri": uri,
                    "version": version
                },
                "contentChanges": [
                    {
                        "text": text
                    }
                ]
            }
        }

    def getCompletionRequest(self, uri,line, char):
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "textDocument/completion",
            "params": {
                "textDocument": {
                    "uri": uri
                },
                "position": {
                    "line": line,
                    "character": char
                }
            }
        }

    def getHoverRequest(self, uri, line, char):
        return {
            "jsonrpc": self.jsonrpc,
            "id": 2,
            "method": "textDocument/hover",
            "params": {
                "textDocument": {
                    "uri": uri
                },
                "position": {
                    "line": line,
                    "character": char
                }
            }
        }

  