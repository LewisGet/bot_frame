import tensorflow as tf
from tensorflow.contrib.layers import conv2d
from tensorflow.contrib.layers import max_pool2d
from tensorflow.contrib.layers import flatten
from tensorflow.contrib.layers import fully_connected

import config


class Net:
    def __init__(self, dataset, learning_rate):
        self.dataset = dataset
        self.learning_rate = learning_rate

        self.input = tf.placeholder(tf.float16, [None, config.input_size[0], config.input_size[1], 3], name='input')
        self.label = tf.placeholder(tf.int8, [None, len(config.labels)], name='label')

        self.logits = self.load_model()

        self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.logits, labels=self.label), name='cost')
        self.optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate, name='adam').minimize(self.cost)

        self.correct_pred = tf.equal(tf.argmax(self.model, 1), tf.argmax(self.label, 1))
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_pred, tf.float16), name='accuracy')

    def load_model(self):
        # 1st
        conv1 = conv2d(self.input, num_outputs=96,
                       kernel_size=[11, 11], stride=4, padding="VALID",
                       activation_fn=tf.nn.relu)
        lrn1 = tf.nn.local_response_normalization(conv1, bias=2, alpha=0.0001, beta=0.75)
        pool1 = max_pool2d(lrn1, kernel_size=[3, 3], stride=2)

        # 2nd
        conv2 = conv2d(pool1, num_outputs=256,
                       kernel_size=[5, 5], stride=1, padding="VALID",
                       biases_initializer=tf.ones_initializer(),
                       activation_fn=tf.nn.relu)
        lrn2 = tf.nn.local_response_normalization(conv2, bias=2, alpha=0.0001, beta=0.75)
        pool2 = max_pool2d(lrn2, kernel_size=[3, 3], stride=2)

        # 3rd
        conv3 = conv2d(pool2, num_outputs=384,
                       kernel_size=[3, 3], stride=1, padding="VALID",
                       activation_fn=tf.nn.relu)

        # 4th
        conv4 = conv2d(conv3, num_outputs=384,
                       kernel_size=[3, 3], stride=1, padding="VALID",
                       biases_initializer=tf.ones_initializer(),
                       activation_fn=tf.nn.relu)

        # 5th
        conv5 = conv2d(conv4, num_outputs=256,
                       kernel_size=[3, 3], stride=1, padding="VALID",
                       biases_initializer=tf.ones_initializer(),
                       activation_fn=tf.nn.relu)
        pool5 = max_pool2d(conv5, kernel_size=[3, 3], stride=2)

        # 6th
        flat = flatten(pool5)
        fcl1 = fully_connected(flat, num_outputs=4096,
                               biases_initializer=tf.ones_initializer(), activation_fn=tf.nn.relu)
        dr1 = tf.nn.dropout(fcl1, 0.5)

        # 7th
        fcl2 = fully_connected(dr1, num_outputs=4096,
                               biases_initializer=tf.ones_initializer(), activation_fn=tf.nn.relu)
        dr2 = tf.nn.dropout(fcl2, 0.5)

        # output
        out = fully_connected(dr2, num_outputs=self.num_classes, activation_fn=None)
        return out

    def train(self, x, y, vx, vy, epochs, times):
        with tf.Session() as sess:
            print('global_variables_initializer...')
            sess.run(tf.global_variables_initializer())

            print('starting training ... ')

            for i in range(times):
                for epoch in range(epochs):
                    _ = sess.run(self.optimizer, feed_dict={input: x, label: y})
                    print('Epoch %d : ' % epoch)

                valid_acc = sess.run(self.accuracy, feed_dict={input: vx, label: vy})
                print("accuracy %f" % valid_acc)

            # Save Model
            saver = tf.train.Saver()
            save_path = saver.save(sess, config.save_model_path)
