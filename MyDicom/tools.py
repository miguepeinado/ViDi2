"""
Different tools to use with pydicom or dicom images
"""


def in_(data_set, key):
    """Search an element in a pydicom dataset

    :param data_set:
    :param key: keyword of the element
    :return: The element found (if any) and a path with sequences containing it (if it's nested)
    """

    import dicom

    def search_helper(ds, k, p):
        """
        :param ds: dataset to search into
        :param k: key to search
        :param p: path to fill in recursion
        :return: element found (if any)
        """
        if k in ds:
            # Normal case
            tag = dicom.datadict.tag_for_name(k)
            return ds[tag], p
        for el in ds:
            if el.VR == 'SQ':
                values = el.value
                i = 0
                for ds in values:
                    element, path = search_helper(ds, k, p)
                    i += 1
                    if element is not None:
                        p.append([el.tag, i - 1])
                        return element, path
        return None, p

    path = []
    element, path = search_helper(data_set, key, path)
    if element is not None:
        return element, path.reverse()
    raise KeyError("{0} not present in dataset".format(key))