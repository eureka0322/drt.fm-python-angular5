class SerializerRequestSwitchMixin(object):
    serializer_classes = {}

    def get_serializer_class(self):
        if hasattr(self.request, 'QUERY_PARAMS'):
            serializer = self.request.QUERY_PARAMS.get('serializer', 'default')
        else:
            serializer = self.request.GET.get('serializer', 'default')
        if serializer in self.serializer_classes:
            self.serializer_name = serializer
            return self.serializer_classes.get(serializer)
        return super(SerializerRequestSwitchMixin, self).get_serializer_class()

    def get_serializer_name(self):
        return self.serializer_name
