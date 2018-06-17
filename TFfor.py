import tensorflow as tf
import dataset_util

import cv2
tf.app.flags.DEFINE_string('FLA','./rawdata/tf',"dec")

FLAGS = tf.app.flags.FLAGS


def create_tf_example():

  height = 544 # Image height
  width = 960 # Image width
  filename = 'Image10.jpg' # Filename of the image. Empty if image is not from file
  filename=filename.encode()
  with tf.gfile.GFile("./Image10.jpg", 'rb') as fid:
        encoded_image = fid.read()
  image_format = b'jpg' # b'jpeg' or b'png'

  xmins = [458.0/960.0] # List of normalized left x coordinates in bounding box (1 per box)
  xmaxs = [807.0/960.0] # List of normalized right x coordinates in bounding box
             # (1 per box)
  ymins = [157.0/544.0] # List of normalized top y coordinates in bounding box (1 per box)
  ymaxs = [360.0/544.0] # List of normalized bottom y coordinates in bounding box
             # (1 per box)
  classes_text = b"library" # List of string class name of bounding box (1 per box)
  #classes_text=classes_text.encode("utf8")
  classes = "2" # List of integer class id of bounding box (1 per box)
  classes=classes.encode()
  tf_example = tf.train.Example(features=tf.train.Features(feature={
      'image/height': dataset_util.int64_feature(height),
      'image/width': dataset_util.int64_feature(width),
      'image/filename': dataset_util.bytes_feature(filename),
      'image/source_id': dataset_util.bytes_feature(filename),
      'image/encoded': dataset_util.bytes_feature(encoded_image),
      'image/format': dataset_util.bytes_feature(image_format),
      'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
      'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
      'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
      'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
      #'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
      'image/object/class/label': dataset_util.int64_list_feature(classes),
  }))
  return tf_example


def main(_):
  writer = tf.python_io.TFRecordWriter(FLAGS.FLA)
  tf_example = create_tf_example()
  writer.write(tf_example.SerializeToString())
  # TODO(user): Write code to read in your dataset to examples variable

#  for example in examples:
#    tf_example = create_tf_example(example)
#    writer.write(tf_example.SerializeToString())

  writer.close()


if __name__ == '__main__':
  tf.app.run()
