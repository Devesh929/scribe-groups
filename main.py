# coding=utf-8
import logging
from flask import Flask, request, jsonify
import warnings
from yapsy.PluginManager import PluginManager

app = Flask(__name__)

@app.route('/', methods=['GET'])
def process_text():
    if not request.json or not 'transcript' in request.json:
        abort(400)
    transcript = request.json['transcript']
    # Initialize the plugin manager.
    simplePluginManager = PluginManager()
    simplePluginManager.setPluginPlaces(["./plugins"])
    simplePluginManager.getPluginLocator().setPluginInfoExtension('plugin.info')
    # Load and activate plugins.
    simplePluginManager.collectPlugins()
    response = { }
    for pluginInfo in simplePluginManager.getAllPlugins():
        returnValue = pluginInfo.plugin_object.process(transcript)
        response.update(returnValue)

    return jsonify(response), 200

if __name__ == '__main__':
  app.run()
