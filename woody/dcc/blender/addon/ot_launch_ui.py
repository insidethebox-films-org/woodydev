import bpy
import socket
import json

CONTROL_PORT = 6001

class WOODY_OT_launch_UI(bpy.types.Operator):
    bl_idname = "woody.launch_ui"
    bl_label = "Launch Woody UI"
    bl_description = "Launch the Woody external UI"

    def execute(self, context):
        # Try to tell an existing Woody instance to show/raise the DccGui window
        # via the control socket. If that fails, report an error (user should
        # start Woody first or we could try to launch it).
        try:
            s = socket.create_connection(("127.0.0.1", CONTROL_PORT), timeout=1)
            msg = {"command": "show_dcc_gui"}
            s.sendall(json.dumps(msg).encode("utf8"))
            resp = s.recv(4096)
            try:
                data = json.loads(resp.decode("utf8"))
                if data.get("status") == "ok":
                    self.report({'INFO'}, "DCC UI shown/created.")
                else:
                    self.report({'WARNING'}, f"Woody control: {data.get('message')}")
            except Exception:
                self.report({'WARNING'}, "Woody control: invalid response")
            s.close()
            return {'FINISHED'}
        except Exception as e:
            # Couldn't contact the running Woody app.
            self.report({'ERROR'}, "Woody app not running. Please start Woody first.")
            return {'CANCELLED'}